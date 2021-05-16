const execa = require('execa');
const { resolve } = require('path');
const pyPath = resolve(__dirname, './NOLevelPy/HLWP1_main.py');
module.exports = async ({ minlat, maxlat, minlon, maxlon }, year, month) => {
  const { stdout } = await execa(
    `python ${pyPath} --minlat ${minlat} --maxlat ${maxlat} --minlon ${minlon} --maxlon ${maxlon} --year ${year} --month ${month}`
  );
  return JSON.parse(stdout);
}