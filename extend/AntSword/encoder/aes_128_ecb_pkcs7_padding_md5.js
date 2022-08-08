'use strict';

const path = require('path');
var CryptoJS = require(path.join(window.antSword.remote.process.env.AS_WORKDIR, 'node_modules/crypto-js'));

function encryptText(keyStr, text) {
  let buff = Buffer.alloc(16, 'a');
  buff.write(keyStr,0);
  keyStr = buff.toString();
  let encodetext = CryptoJS.AES.encrypt(text, CryptoJS.enc.Utf8.parse(keyStr), {
    mode: CryptoJS.mode.ECB,
    padding: CryptoJS.pad.Pkcs7,
  }).toString();
  return encodetext;
}

module.exports = (pwd, data) => {
    let str = Buffer.from(data['_']).toString();
    let key = CryptoJS.MD5(pwd).toString().substr(0, 16);
    data[pwd] = Buffer.from(encryptText(key, str), 'binary');
    delete data['_'];
    return data;
}