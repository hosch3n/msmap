# AES-128-ECB-PKCS7-MD5
code = """
    private byte[] cipher(
            byte[] payload, String alg, byte[] key, boolean isEnc
    ) {
        try {
            javax.crypto.Cipher c = javax.crypto.Cipher.getInstance(alg);
            c.init(isEnc?1:2, new javax.crypto.spec.SecretKeySpec(key, alg));
            return c.doFinal(payload);
        } catch (Exception e) {
            return null;
        }
    }

    private String hasher(String str, String alg) {
        try {
            java.security.MessageDigest h =
                java.security.MessageDigest.getInstance(alg);
            h.update(str.getBytes(), 0, str.length());
            return new java.math.BigInteger(1, h.digest()).toString(16);
        } catch (Exception e) {
            return null;
        }
    }

    private byte[] decoder(String payload) {
        return cipher(
            b64decode(payload), "AES",
            hasher(password, "MD5").substring(0, 16).getBytes(), false
        );
    }
"""