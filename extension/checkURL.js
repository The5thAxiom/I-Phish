const tags = tag => Array.from(document.getElementsByTagName(tag));

/*
type Link {
    tag: HtmlELement;
    href: string;
    hasError: boolean;
    isBenign: boolean;
};
*/

function saveToCache(url, hasError, isBenign) {
    const alreadyInCache = localStorage.getItem(url);
    if (!alreadyInCache)
        localStorage.setItem(url, JSON.stringify({ hasError, isBenign }));
}

function checkCache(url) {
    const cachedValue = JSON.parse(localStorage.getItem(url));
    return { inCache: !!cachedValue, result: cachedValue };
}

async function validateURL(url) {
    const { inCache, result } = checkCache(url);
    if (inCache) return result;
    
    const apiURL = 'http://127.0.0.1:8000';
    const resp = await fetch(apiURL + '/is-valid-url', {
        method: 'POST',
        body: JSON.stringify({ url }),
        headers: { 'Content-Type': 'application/json' }
    });
    let hasError = false;
    let isBenign = false;
    if (!resp.ok) hasError = true;
    else {
        const data = await resp.json();
        if (data.msg !== 'OK') alert(`${url}: ${data.msg}`);
        isBenign = data.isBenign;
    }
    saveToCache(url, hasError, isBenign);
    return { hasError, isBenign };
}

// converting any relative URLs to absolute URLs
function cleanLink(href) {
    let url;
    try {
        url = new URL(href);
    } catch (e) {
        url = new URL(href, document.baseURI);
    }
    return url.href;
}

async function main() {
    const links = tags('a').map(tag => ({
        tag,
        href: cleanLink(tag.getAttribute('href'))
    }));

    // set each link to be in the 'loading' state
    links.forEach(({ tag }) => {
        tag.classList.remove('iphish-malicious');
        tag.classList.remove('iphish-benign');
        tag.classList.remove('iphish-unknown');
        tag.classList.add('iphish-loading');
    });

    // now, for each link:
    links.forEach(async ({ tag, href }) => {
        // we validate the URL as being benign or malicious from the API
        const { hasError, isBenign } = await validateURL(href);

        // we remove the loading state from each link
        tag.classList.remove('iphish-loading');

        // and add the new state based on the API response
        if (hasError) tag.classList.add('iphish-unkown');
        else if (isBenign) tag.classList.add('iphish-benign');
        else tag.classList.add('iphish-malicious');
    });
}

main();
