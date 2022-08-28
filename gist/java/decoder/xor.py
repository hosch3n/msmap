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