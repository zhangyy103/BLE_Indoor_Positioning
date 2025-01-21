(function($, global) {

	var registered = false;
	var visible = false;

	function init(context) {
		if (context.indicator) {
			return;
		}

		context.indicator = $($.telligent.evolution.template(context.template)({}))
			.hide()
			.appendTo('body');
	}

	function indicateDisconnection(context, reconnecting) {
		init(context);

		visible = true;

		context.indicator.attr('data-tip', reconnecting
			? context.disconnect
			: context.permanentDisconnect);

		context.indicator
			.removeClass('online')
			.addClass('offline')
			.fadeIn(200);
	}

	function indicateReconnection(context) {
		if (!visible) {
			return;
		}

		visible = false;

		init(context);

		context.indicator
			.removeClass('offline')
			.addClass('online');
		context.indicator.attr('data-tip', context.reconnect);

		global.setTimeout(function() {
			context.indicator.fadeOut(200);
		}, 5000);
	}

	var api = {
		register: function(context) {
			if ((global.parent && global.parent != global) || registered) {
				return;
			}

			registered = true;

			$.telligent.evolution.messaging.subscribe('socket.disconnected', function(data) {
				indicateDisconnection(context, data.reconnecting);
			}, { excludeAutoNameSpaces: true });

			$.telligent.evolution.messaging.subscribe('socket.reconnected', function(){
				indicateReconnection(context);
			}, { excludeAutoNameSpaces: true });
		}
	};

	$.telligent = $.telligent || {};
	$.telligent.evolution = $.telligent.evolution || {};
	$.telligent.evolution.widgets = $.telligent.evolution.widgets || {};
	$.telligent.evolution.widgets.offlineIndicator = api;

}(jQuery, window));