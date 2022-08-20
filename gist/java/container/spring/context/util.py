code = """
    private Object getWebApplicationContext() throws Exception {
        Class requestContextHolder = Class.forName(
            "org.springframework.web.context.request.RequestContextHolder"
        );
        Object servletRequestAttributes = getMethodX(
            requestContextHolder, "currentRequestAttributes", 0
        ).invoke(requestContextHolder);
        Object request = getMethodX(
            servletRequestAttributes.getClass(), "getRequest", 0
        ).invoke(servletRequestAttributes);

        Class requestContextUtils = Class.forName(
            "org.springframework.web.servlet.support.RequestContextUtils"
        );
        return getMethodX(
            requestContextUtils, "findWebApplicationContext", 1
        ).invoke(requestContextUtils, request);
    }
"""