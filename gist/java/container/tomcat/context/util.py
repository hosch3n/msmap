code = """
    private Object getStandardContext() throws Exception {
        Object standardContext = invokeMethod(
                getFieldValue(getLoader(), "resources"),
                "getContext"
        );

        if (standardContext != null) {
            return standardContext;
        }

        Class applicationDispatcher = Class.forName(
            "org.apache.catalina.core.ApplicationDispatcher"
        );
        Class applicationFilterChain = Class.forName(
            "org.apache.catalina.core.ApplicationFilterChain"
        );

        Field wrap = getField(applicationDispatcher, "WRAP_SAME_OBJECT");
        Field lastServicedRequest = getField(
            applicationFilterChain, "lastServicedRequest"
        );
        Field lastServicedResponse = getField(
            applicationFilterChain, "lastServicedResponse"
        );

        ThreadLocal servletRequest =
            (ThreadLocal) lastServicedRequest.get(null);
        if (servletRequest == null) {
            lastServicedRequest.set(null, new ThreadLocal());
            lastServicedResponse.set(null, new ThreadLocal());
            wrap.setBoolean(null, true);
        }
        return getFieldValue(getFieldValue(invokeMethod(
            servletRequest.get(), "getServletContext"
        ), "context"), "context");
    }
"""