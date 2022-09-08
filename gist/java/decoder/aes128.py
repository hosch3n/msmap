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

proc = """
            Class base64;
            Object decoder;
            byte[] bytes = null;
            java.security.MessageDigest h;
            javax.crypto.Cipher c;

            try {
                base64 = Class.forName("java.util.Base64");
                decoder = base64.getMethod("getDecoder")
                    .invoke(base64);
                bytes = (byte[]) decoder.getClass()
                    .getMethod("decode", String.class)
                    .invoke(decoder, payload);
            } catch (ClassNotFoundException e) {
                try {
                    base64 = Class.forName("sun.misc.BASE64Decoder");
                    decoder = base64.newInstance();
                    bytes = (byte[]) decoder.getClass()
                        .getMethod("decodeBuffer", String.class)
                        .invoke(decoder, payload);
                } catch (Exception ex) {}
            } catch (Exception ex) {}

            h = java.security.MessageDigest.getInstance("MD5");
            h.update(password.getBytes(), 0, password.length());
            byte[] key = new BigInteger(1, h.digest()).toString(16)
                .substring(0, 16).getBytes();

            c = javax.crypto.Cipher.getInstance("AES");
            c.init(2, new javax.crypto.spec.SecretKeySpec(key, "AES"));
            bytes = c.doFinal(bytes);
"""