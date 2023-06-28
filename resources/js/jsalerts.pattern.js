import $ from "jquery";
import Base from "@patternslib/patternslib/src/core/base";
import MD5 from "crypto-js/md5";
import "jquery.cookie";
import("./jsalerts.scss");


export default Base.extend({
    // The name for this pattern
    name: 'alertmessage',
    trigger: '.pat-alertmessage',
    parser: 'mockup',
    defaults: {
        'get_message_view': '/get-alert-message',
        'show_in_context': true,
        'cache': false
    },

    set_cookie: function(data, action){
      var self = this;
      var cookie_expire = data.cookie_expire ? data.cookie_expire : 0;
      var cookie_expire_minimize = data.cookie_expire_minimize ? data.cookie_expire_minimize : 0;

      if (action === 'minimize' && (cookie_expire_minimize === 0 || isNaN(parseFloat(cookie_expire_minimize)))){
        return;
      }
      if (action === 'close' && (cookie_expire === 0 || isNaN(parseFloat(cookie_expire)))){
        return;
      }

      var md5_key = data.alert_location + data.title + data.cookie_expire + data.cookie_expire_minimize + data.display_on_every_page + data.klass + data.message + data.retract_timeout + data.date;

      var val = MD5(md5_key);
      var date = new Date();
      if (action == 'close'){
        date.setTime(date.getTime() + (cookie_expire * 60 * 60 * 1000));
      }
      if (action == 'minimize'){
        date.setTime(date.getTime() + (cookie_expire_minimize * 60 * 60 * 1000));
      }

      $.cookie("alert.message."+action+"."+val.toString().slice(20), "1", { expires: date, path: '/' });
    },

    is_visible: function(data){
      var self = this;
      var should_show = false;
      if (data.visible){
        // Emergency message visible, now check cookie
        var md5_key = data.alert_location + data.title + data.cookie_expire + data.cookie_expire_minimize + data.display_on_every_page + data.klass + data.message + data.retract_timeout + data.date;
        var val = MD5(md5_key);
        var close_cookie = $.cookie("alert.message.close."+val.toString().slice(20));

        if (close_cookie === undefined){
          // No cookie, now check if should be seen at homepage only
          var display_on_every_page;
          if (data.display_on_every_page === undefined){
            // By default show on every page, unless explicitly denied
            display_on_every_page = true;
          }
          else{
            display_on_every_page = data.display_on_every_page;
          }

          if (display_on_every_page){
            // This message should be displayed everywhere
            should_show = true;
          }
          else{
            should_show = self.options.show_in_context;
          }

        }
        // Cookie was present, so we are not going to show the message
      }

      return should_show;
    },

    show_on_top: function(data){
        var self = this;
        var div = $('<div class="alert alert-'+data.klass+' alert-dismissible" role="alert"></div>');

        if(window.innerWidth <= 769) {
          div.addClass("mobile");
        }

        var close = $('<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>')
                    .on('click', function () {
                        self.$el.html("");
                        self.set_cookie(data, 'close');
                    });;

        var msg = $('<div></div>');
        if (data.title !== ""){
          msg.append($('<strong>'+data.title+': </strong>'));
        }
        if (data.message !== ""){
          msg.append($('<span>'+data.message+'</span>'));
        }
        div.append(close);
        div.append(msg);

        self.$el.html("");
        self.$el.append(div);

        if (data.retract_timeout !== 0){
            setTimeout(function() {
                div.remove();
            }, data.retract_timeout * 1000);
        }
    },

    show_slide: function(data, direction){
      var self = this;

      var slide_box = $('<div class="slide-alert-message"></div>');
      slide_box.addClass(direction);
      slide_box.addClass('alert-'+data.klass);

      if(window.innerWidth <= 769) {
        slide_box.addClass("mobile");
      }

      var minimize = $('<button type="button" aria-label="Minimize" class="close minimize"><span aria-hidden="true">&nbsp;-</span></button>')
                  .on('click', function () {
                      self.set_cookie(data, 'minimize');
                      if (slide_box.hasClass('visible')){
                        slide_box.removeClass('visible');
                        clearTimeout(timeout);
                      }
                  });

      var close = $('<button type="button" aria-label="Close" class="close"><span aria-hidden="true">&times;</span></button>')
                  .on('click', function () {
                      self.$el.html("");
                      self.set_cookie(data, 'close');
                  });

      var msg = $('<div></div>');
      if (data.message !== ""){
        msg.append($('<span>'+data.message+'</span>'));
      }
      slide_box.append(close);
      slide_box.append(minimize);
      slide_box.append(msg);

      self.$el.html("");
      self.$el.append(slide_box);

      var timeout;
      /* Trigger button to slide the notification open */
      var trigger_tab = $('<span class="btn open-slide-alert-message" aria-label="Open"></button>')
                        .on('click', function () {
                          if (slide_box.hasClass('visible')){
                            slide_box.removeClass('visible');
                            clearTimeout(timeout);
                          }
                          else{
                            slide_box.addClass('visible');
                            if (data.retract_timeout !== 0){
                                timeout = setTimeout(function() {
                                    slide_box.removeClass('visible');
                                }, data.retract_timeout * 1000);
                            }
                          }
                        });

      trigger_tab.addClass(direction);
      trigger_tab.addClass('alert-'+data.klass);
      trigger_tab.html(data.title ? data.title : data.klass);
      self.$el.append(trigger_tab);

      var md5_key = data.alert_location + data.title + data.cookie_expire + data.cookie_expire_minimize + data.display_on_every_page + data.klass + data.message + data.retract_timeout + data.date;
      var val = MD5(md5_key);
      var minimize_cookie = $.cookie("alert.message.minimize."+val.toString().slice(20));
      if (minimize_cookie === undefined){
        /* Only open the notification if there is no cookie */
        trigger_tab.trigger('click');
      }

    },

    init: function() {
      if (window.location.pathname.includes("@@set-alert-message")){
          return;
      }
      var self = this;
      $.ajax({
        url:      self.options.get_message_view,
        type:     'GET',
        context:  self.$el,
        async:    true,
        cache:    self.options.cache
      }).done(function(data, status, xhr) {
        if (!self.is_visible(data)){
          return;
        }
        if (data.alert_location === 'fixed_top'){
          self.show_on_top(data);
        } else if (data.alert_location === 'slide_left'){
          self.show_slide(data, 'left');
        } else if (data.alert_location === 'slide_right'){
          self.show_slide(data, 'right');
        } else if (data.alert_location === 'slide_top'){
          self.show_slide(data, 'top');
        }
      });
    }
  });
