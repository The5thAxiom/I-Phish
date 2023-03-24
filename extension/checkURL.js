const tags = tag => Array.from(document.getElementsByTagName(tag));

/*
type Link {
    tag: HtmlELement;
    href: string;
    hasError: boolean;
    isValid: boolean;
};
*/

async function validateURLS(links) {
    // links: Link[]

    // sleep for 2 sec
    await new Promise(r => setTimeout(r, 2000));
    return links.map(tagData => ({
        ...tagData,
        hasError: Math.random() < 0.3,
        isValid: Math.random() < 0.5
    }));
}

function cleanLink({ tag, href }) {
    return { tag, href: href && cleanLink(href) };
}

function styleTag({ tag, hasError, isValid }) {
    tag.style.color = hasError ? 'gray' : isValid ? 'green' : 'red';
    tag.style.cursor = hasError ? 'help' : isValid ? 'pointer' : 'not-allowed';
    tag.style.textDecoration = hasError
        ? 'underline'
        : isValid
        ? 'none'
        : 'underline';
    tag.style.textDecorationStyle = hasError ? 'dashed' : isValid ? '' : 'wavy';
}

async function main() {
    const links = tags('a')
        .map(tag => ({
            tag: tag,
            href: tag.getAttribute('href')
        }))
        .map(cleanLink);
    links.forEach(({ tag }) => {
        tag.style.color = 'gray';
        tag.style.cursor = 'wait';
    });
    const validatedLinks = await validateURLS(links);
    validatedLinks.forEach(styleTag);
}

main();
