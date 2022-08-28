'use strict';

const path = require('path');
var CryptoJS = require(path.join(
  window.antSword.remote.process.env.AS_WORKDIR, 'node_modules/crypto-js'
));

function aes(key, text) {
  let buff = Buffer.alloc(16, 'a');
  buff.write(key, 0);
  key = buff.toString();
  let cipher = CryptoJS.AES.encrypt(text, CryptoJS.enc.Utf8.parse(key), {
    mode: CryptoJS.mode.ECB,
    padding: CryptoJS.pad.Pkcs7,
  }).toString();
  return cipher;
}

module.exports = (pwd, data) => {
    let str = Buffer.from(data['_']).toString();
    let key = CryptoJS.MD5(pwd).toString().substr(0, 16);
    data[pwd] = Buffer.from(aes(key, str), 'binary');
    delete data['_'];
    return data;
}