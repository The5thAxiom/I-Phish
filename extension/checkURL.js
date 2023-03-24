const tags = tag => Array.from(document.getElementsByTagName(tag));

/*
type Link {
    tag: HtmlELement;
    href: string;
    hasError: boolean;
    isValid: boolean;
};
*/

async function validateURL(url) {
    const apiURL = 'http://127.0.0.1:8000';
    const resp = await fetch(apiURL + '/is-valid-url', {
        method: 'POST',
        body: JSON.stringify({ url }),
        headers: { 'Content-Type': 'application/json' }
    });
    let hasError = false;
    let isValid = false;
    if (!resp.ok) hasError = true;
    else {
        const data = await resp.json();
        if (data.msg !== 'OK') alert(`${url}: ${data.msg}`);
        isValid = data.ans;
    }
    return { hasError, isValid };
}

function cleanLink(href) {
    return href;
}

function styleTag(tag, hasError, isValid) {
    tag.style.color = hasError ? 'gray' : isValid ? 'green' : 'red';
    tag.style.cursor = hasError ? 'help' : isValid ? 'pointer' : 'not-allowed';
    tag.style.textDecoration = 'underline';
    tag.style.textDecorationStyle = hasError
        ? 'dashed'
        : isValid
        ? 'solid'
        : 'wavy';
}

async function main() {
    const links = tags('a').map(tag => ({
        tag,
        href: cleanLink(tag.getAttribute('href'))
    }));

    links.forEach(({ tag }) => {
        tag.style.cursor = 'wait';
    });

    links.forEach(async ({ tag, href }) => {
        const { hasError, isValid } = await validateURL(href);
        styleTag(tag, hasError, isValid);
    });
}

main();
