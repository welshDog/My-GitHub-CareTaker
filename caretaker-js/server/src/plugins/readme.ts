export function generateBannerSVG(repo:string){
  return `<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="240">\n<rect width="100%" height="100%" fill="#1a1f29"/>\n<text x="50" y="120" fill="#a3bffa" font-size="48" font-family="Arial">${repo}</text>\n</svg>`
}

export function readmeHeader(repo:string, badges:{build?:string, version?:string, downloads?:string, license?:string}){
  const svg = generateBannerSVG(repo)
  return {
    svg,
    markdown: `![Banner](./.caretaker/banner.svg)\n\n${badges.build ? `![Build](${badges.build}) ` : ''}${badges.version ? `![Version](${badges.version}) ` : ''}${badges.downloads ? `![Downloads](${badges.downloads}) ` : ''}${badges.license ? `![License](${badges.license})` : ''}`
  }
}
