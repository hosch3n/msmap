'use strict';

const path = require('path');
var CryptoJS = require(path.join(
    window.antSword.remote.process.env.AS_WORKDIR, 'node_modules/crypto-js'
));

function xor(pwd, data) {
  let key = pwd.split("").map((t) => t.charCodeAt(0));
  let cipher = data.split("").map((t) => t.charCodeAt(0));
  for (let i = 0; i < cipher.length; i++) {
    cipher[i] = cipher[i] ^ key[i + 1 & 15];
  }
  cipher = cipher.map((t) => String.fromCharCode(t)).join("");
  return cipher;
}

module.exports = (pwd, data) => {
  let str = Buffer.from(data['_']).toString();
  let key = CryptoJS.MD5(pwd).toString().substr(0, 16);
  data[pwd] = Buffer.from(xor(key, str), 'binary').toString('base64');
  delete data['_'];
  return data;
}