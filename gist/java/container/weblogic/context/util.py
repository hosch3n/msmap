code = """
    private Object getWebAppServletContext() throws Exception {
        Object workEntry = getFieldValue(Thread.currentThread(), "workEntry");
        Object wm = getFieldValue(workEntry, "wm");
        Object runtimeAccess = getFieldValue(wm, "runtimeAccess");
        Iterator mBeanImpls = ((java.util.concurrent.ConcurrentMap)
                getFieldValue(runtimeAccess, "configToRuntimeBean"))
                .entrySet().iterator();
        while (mBeanImpls.hasNext()) {
            Map.Entry mBeanImpl = (Map.Entry) mBeanImpls.next();
            try {
                if (getFieldValue(
                        mBeanImpl.getKey(), "_ContextPath").equals(pattern)
                ) {
                    return getFieldValue(mBeanImpl.getValue(), "context");
                }
            } catch (Exception e) {}
        }
        return null;
    }
"""