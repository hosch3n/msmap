'use strict';

const path = require('path');
var CryptoJS = require(path.join(
    window.antSword.remote.process.env.AS_WORKDIR, 'node_modules/crypto-js'
));

function rc4(key, data) {
    let pwd = key;
    let cipher = '';
    key = [];
    let box = [];
    let pwd_length = pwd.length;
    let data_length = data.length;
    for (var i = 0; i < 256; i++) {
        key[i] = pwd[i % pwd_length].charCodeAt();
        box[i] = i;
    }
    for (var j = i = 0; i < 256; i++) {
        j = (j + box[i] + key[i]) % 256;
        var tmp = box[i];
        box[i] = box[j];
        box[j] = tmp;
    }
    for (var a = j = i = 0; i < data_length; i++) {
        a = (a + 1) % 256;
        j = (j + box[a]) % 256;
        tmp = box[a];
        box[a] = box[j];
        box[j] = tmp;
        let k = box[((box[a] + box[j]) % 256)];
        cipher += String.fromCharCode(data[i].charCodeAt() ^ k);
    }
    return cipher;
}

module.exports = (pwd, data) => {
    let str = Buffer.from(data['_']).toString();
    let key = CryptoJS.SHA256(pwd).toString();
    data[pwd] = Buffer.from(rc4(key, str), 'binary').toString('base64');
    delete data['_'];
    return data;
}