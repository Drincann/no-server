const execa = require('execa');
const { resolve } = require('path');
const pyPath = resolve(__dirname, './NOLevelPy/HLWP1_main.py');
module.exports = /*fun =*/ async ({ minlat, maxlat, minlon, maxlon }, year, month) => {
  const { stdout } = await execa(
    `python ${pyPath} --minlat ${minlat} --maxlat ${maxlat} --minlon ${minlon} --maxlon ${maxlon} --year ${year} --month ${month}`
  );
  const json = JSON.parse(stdout);
  // require('fs').writeFileSync('./a.jpg', Buffer.from(json.imgBase64, 'base64'))
  return json;
}

// fun({ minlat: 35.5, maxlat: 37.5, minlon: 119.9, maxlon: 121.9 }, 2019, 1)