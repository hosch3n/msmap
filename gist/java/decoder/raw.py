code = """
    private byte[] decoder(String payload) {
        return payload.getBytes();
    }
"""

proc = """
            Class base64;
            Object decoder;
            byte[] bytes = payload.getBytes();
"""