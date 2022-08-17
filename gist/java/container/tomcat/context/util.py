code = """
    private Object getStandardContext() {
        return invokeMethod(
            getFieldValue(getLoader(), "resources"),
            "getContext"
        );
    }
"""