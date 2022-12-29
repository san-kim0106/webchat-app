$(function() {
    var conn = null;
    var name = "UNKNOWN";

    function log(data, flag) {
        var date = new Date();
        var date_prompt = '(' + date.toISOString().split('T')[1].slice(0,6) + ') ';

        switch (flag) {
            case "date":
                $("convo").html(`
                <div class="date-divider">
                    <span class="date-divider__text">Wednesday, March 18, 2019</span>
                </div>
                `.format(data.name))
                break;

            case 'join':
                $("convo").html(`
                <div class="join-msg">{} joined this chatroom</div>
                `.format(data.name))
                break;

            case "sent_to_me":
                $("convo").html(`
                <div class="chat__message chat__message--to-me">
                    <div class="chat__message-center">
                        <h3 class="chat__message-username">{0}</h3>
                    </div>
                    <span class="chat__message-body">{1}</span>
                    <span class="chat__message-time">19:25</span>
                </div>
                `.format(data.name, data.text))
                break;
            
            case "sent_from_me":
                $("convo").html(`
                <div class="chat__message chat__message--from-me">
                    <span class="chat__message-time">17:55</span>
                    <span class="chat__message-body">{}</span>
                </div>
                `.format(data.text))
                break;

            case 'left':
                $("convo").html(`
                <div class="join-msg">{} left this chatroom</div>
                `.format(data.name))
                break;
        }
    }

    function connect() {
        conn = new WebSocket("ws://localhost:8080");

        conn.onmessage = function(e) {
            var data = JSON.parse(e.data);
            switch (data.action) {
                case "date":
                    log(data, "date");
                    break;
                case 'join':
                    log(data, "join");
                    break;
                case "sent_to_me":
                    log(data, "sent_to_me");
                    break;
                case "sent_from_me":
                    log(data, "sent_from_me");
                    break;
                case 'left':
                    log(data, "left");
                    break;
            }
        };

        conn.onclose = function() {
            log({name: "Foo"}, "left");
            conn = null;
        };
    }
    
    function disconnect() {
        if (conn != null) {
            //log('Disconnecting...');
            conn.close();
            conn = null;
            name = 'UNKNOWN';
            update_ui();
      }
    }

    $('.send').on('click', function() {
        var msg = $('#msg').val();
        log({text: msg}, "sent_from_me");
        conn.send(msg);
        $('#text').val('').focus();
        return false;
    });

    $('#text').on('keyup', function(e) {
        if (e.keyCode === 13) {
            $('#send').click();
            return false;
        }
    });
  });