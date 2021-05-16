const execa = require('execa');
const { resolve } = require('path');
const pyPath = resolve(__dirname, './NOLevelPy/HLWP1_main.py');
module.exports = async ({ minlat, maxlat, minlon, maxlon }, year, month) => {
  const { stdout } = await execa(
    `python ${pyPath} --minlat ${minlat} --maxlat ${maxlat} --minlon ${minlon} --maxlon ${maxlon} --year ${year} --month ${month}`
  );
  return JSON.parse(stdout);
}

// let st = Date.now();
// fun({
//   minlat: 36.5,
//   maxlat: 38.5,
//   minlon: 119.9,
//   maxlon: 121.9,
// }, 2019, 1).then((json) => {
//   console.log(Date.now() - st);
//   console.log(json);
//   require('fs').writeFileSync('./a.jpg', Buffer.from(json.imgBase64, 'base64'));
// });

// (async () => {
//   try {
//     var { stdout } = await execa(
//       `python b:\\workspace\\Git\\no-web\\core\\NOLevelPy\\HLWP1_main.py --minlat 36.563808 --maxlat 36.664154 --minlon 114.402726 --maxlon 114.579512 --year 2019 --month 1`
//     );
//   } catch (error) {
//     console.log(error);

//   }

//   require('fs').writeFileSync('./a.jpg', Buffer.from(JSON.parse(stdout).imgBase64), 'base64');
// })()
