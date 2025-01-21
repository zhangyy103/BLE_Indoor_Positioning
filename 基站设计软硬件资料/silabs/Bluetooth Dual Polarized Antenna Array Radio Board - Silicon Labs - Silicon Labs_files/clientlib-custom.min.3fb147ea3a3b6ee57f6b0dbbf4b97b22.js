let imgNodes = document.body.getElementsByTagName("img");
for(let i = 0;i < imgNodes.length; i++)
{
    let imgNode = imgNodes[i];
    if(!imgNode.hasAttribute("alt") || !imgNode.getAttribute("alt")){
        let altText = "";
        if(imgNode.hasAttribute("data-dam-path") && imgNode.getAttribute("data-dam-path")){
        let damPath = imgNode.getAttribute("data-dam-path");
        altText = damPath.split("/").pop().replace(/\.[^/.]+$/, ""); 
        } else if(imgNode.hasAttribute("src")){
        let srcPath = imgNode.getAttribute("src");
        altText = srcPath.split("/").pop().replace(/\.[^/.]+$/, "");
        }
        altText = altText.replace(/-|_/g, ' ');
        if(altText) {
            altText = altText.charAt(0).toUpperCase() + altText.slice(1);
        }
        imgNode.setAttribute("alt", altText);
    }
}

let divNodes = document.body.querySelectorAll('div[data-dam-path]');
for(let i = 0;i < divNodes.length; i++)
{
    let divNode = divNodes[i];
    if(!divNode.hasAttribute("title") || !divNode.getAttribute("title")){
        let altText = "";
        if(divNode.hasAttribute("data-dam-path")){
            let damPath = divNode.getAttribute("data-dam-path");
            altText = damPath.split("/").pop().replace(/\.[^/.]+$/, "");
            altText = altText.replace(/-|_/g, ' ');
            if(altText) {
                altText = altText.charAt(0).toUpperCase() + altText.slice(1);
            }
        }
        divNode.setAttribute("title", altText);
    }
}

let divBgNodes = document.querySelectorAll('div.backgroundcontainer-image');
for(let i = 0;i < divBgNodes.length; i++)
{
    let divBgNode = divBgNodes[i];
    if(!divBgNode.hasAttribute("title") || !divBgNode.getAttribute("title")){
        let url = divBgNode.style.backgroundImage;
        let altText = "";
        if(url){
            let damPath = url.substring(4, url.length-1);
            altText = damPath.split("/").pop().replace(/\.[^/.]+$/, "");
            altText = altText.replace(/-|_/g, ' ');
            if(altText) {
                altText = altText.charAt(0).toUpperCase() + altText.slice(1);
            }
        }
        divBgNode.setAttribute("title", altText);
    }
}

let videoNodes = document.body.querySelectorAll('div[data-video-settings]');
for(let i = 0;i < videoNodes.length; i++)
{
    let videoNode = videoNodes[i];
    if(!videoNode.hasAttribute("title") || !videoNode.getAttribute("title")){
        let altText = "";
        if(videoNode.hasAttribute("data-video-settings")){
            let jsonObj = videoNode.getAttribute("data-video-settings");
            let jsonNode = JSON.parse(jsonObj);
            altText = jsonNode.posterimage.split("/").pop().replace(/\.[^/.]+$/, "");
            altText = altText.replace(/-|_/g, ' ');
            if(altText) {
                altText = altText.charAt(0).toUpperCase() + altText.slice(1);
            }
        }
        videoNode.setAttribute("title", altText);
    }
}