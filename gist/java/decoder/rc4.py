# RC-4-SHA256
code = """
    private byte[] cipher(
            byte[] payload, String alg, byte[] key, boolean isEnc
    ) {
        try {
            StringBuilder hkey = new StringBuilder();
            for (byte b : key) {
                hkey.append(String.format("%02x", b));
            }

            byte[] jkey = hkey.toString().getBytes();
            byte state[] = new byte[256];
            for (int i = 0; i < 256; i++) {
                state[i] = (byte) i;
            }
            int index1 = 0;
            int index2 = 0;
            if (jkey.length == 0) {
                return null;
            }
            for (int i = 0; i < 256; i++) {
                index2 = ((jkey[index1] & 0xff) + (state[i] & 0xff) + index2) & 0xff;
                byte tmp = state[i];
                state[i] = state[index2];
                state[index2] = tmp;
                index1 = (index1 + 1) % jkey.length;
            }

            int x = 0;
            int y = 0;
            byte ikey[] = state;
            int xorIndex;
            byte[] result = new byte[payload.length];
            for (int i = 0; i < payload.length; i++) {
                x = (x + 1) & 0xff;
                y = ((ikey[x] & 0xff) + y) & 0xff;
                byte tmp = ikey[x];
                ikey[x] = ikey[y];
                ikey[y] = tmp;
                xorIndex = ((ikey[x] & 0xff) + (ikey[y] & 0xff)) & 0xff;
                result[i] = (byte) (payload[i] ^ ikey[xorIndex]);
            }
            return result;
        } catch (Exception e) {
            return null;
        }
    }

    private byte[] hasher(String str, String alg) {
        try {
            java.security.MessageDigest h =
                java.security.MessageDigest.getInstance(alg);
            return h.digest(str.getBytes());
        } catch (Exception e) {
            return null;
        }
    }

    private byte[] decoder(String payload) {
        return cipher(
            b64decode(payload), "RC4",
            hasher(password, "SHA-256"), false
        );
    }
"""