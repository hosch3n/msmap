code = """
    private Object getWebApp() throws Exception {
        Class servletInvocation = getLoader()
            .loadClass("com.caucho.server.dispatch.ServletInvocation");
        Object contextRequest = getMethod(
            servletInvocation, "getContextRequest"
        ).invoke(servletInvocation);
        return getMethod(contextRequest.getClass(), "getWebApp")
            .invoke(contextRequest);
    }
"""