code = """
    private String decoder(String payload) {
        payload = new String(b64decode(payload));
        return payload;
    }
"""