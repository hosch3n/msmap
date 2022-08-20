code = """
    private Object getWebApp() throws Exception {
        Class servletInvocation = Class.forName(
            "com.caucho.server.dispatch.ServletInvocation"
        );
        Object contextRequest = getMethod(
            servletInvocation, "getContextRequest"
        ).invoke(servletInvocation);
        return getMethod(contextRequest.getClass(), "getWebApp")
            .invoke(contextRequest);
    }
"""