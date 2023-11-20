require 'socket'
require 'erb'
require 'cgi'

server = TCPServer.new 5678

while session = server.accept
  request = session.gets

  session.print "HTTP/1.0 200\r\n"
  session.print "Content-Type: text/html\r\n"
  session.print "\r\n"

  if request == nil 
    session.close
    next
  end

  path = request[/GET (\/.*?)[? ]/,1]
  if path == "/"
    session.print File.open("index.html").read
  elsif path == "/calc"
    begin
        params = CGI::parse(request[/GET \/.*?\?([^`]*?) /,1])

        q = "Your result is <%=#{params['input'][0]}%>"
        template = ERB.new q 

        session.print template.result(binding)
    rescue Exception, SyntaxError => e
        session.print "500"
    end
  end
  session.close
end