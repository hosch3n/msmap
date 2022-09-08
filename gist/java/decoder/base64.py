code = """
    private byte[] decoder(String payload) {
        return b64decode(payload);
    }
"""

proc = """
            Class base64;
            Object decoder;
            byte[] bytes = null;

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
"""