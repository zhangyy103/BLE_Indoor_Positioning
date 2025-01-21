(function ($, global) {

	// ensures an action only occurs once across all tabs and windows
	//  doOnce(uniqueKey, function() { }, options)
	//  options: (optional)
	//    expireAfter: 5000
	//    maxWait: 500
	var doOnce = (function () {

		var actionsStorageKeyNameSpace = '_unique_actions_',
			get = function (key) {
				return JSON.parse(localStorage.getItem(key));
			},
			set = function (key, value) {
				localStorage.setItem(key, JSON.stringify(value));
			},
			remove = function (key) {
				localStorage.removeItem(key);
			};

		var api = function (key, task, options) {
			var settings = $.extend({
				expireAfter: 5000,
				maxWait: 500
			}, options || {});

			if (!global.localStorage) {
				setTimeout(function () {
					task();
				}, 9);
				return;
			}

			// wait for a small random amount of time to avoid race conditions across tabs
			setTimeout(function () {
				// if no localstorage record exists of this action being taken,
				// record it now and invoke the action
				var actionRecord = get(actionsStorageKeyNameSpace + key);
				if (!actionRecord) {
					set(actionsStorageKeyNameSpace + key, {
						expireAfter: (new Date()).getTime() + settings.expireAfter
					});
					task();
				}
			}, Math.floor(Math.random() * settings.maxWait));
		};

		if (global.localStorage) {
			// garbage-collect action records that happened far enough in the past not to care
			setInterval(function () {
				var currentTime = new Date().getTime();
				for (var i = 0; i < localStorage.length; i++) {
					var actionKey = localStorage.key(i);
					if (actionKey.indexOf(actionsStorageKeyNameSpace) === 0) {
						var actionRecord = get(actionKey);
						if (actionRecord && actionRecord.expireAfter <= currentTime) {
							remove(actionKey);
						}
					}
				}
			}, 1000);
		}

		return api;
	})();

	// var notifier = nativeNotifier();
	// notifier.notify({  });
	//    title: null,
	//    body: null,
	//    iconUrl: null,
	//    tag: null,
	//    onclick: null,
	//    onclose: null,
	//    onshow: null
	var NativeNotifier = (function () {
		var openNativeNotifications = [],
			cleanupRegistered = false;

		function registerUnloadCleanup() {
			if(cleanupRegistered) { return; }
			cleanupRegistered = true;

			$(global).on('unload', function() {
				$.each(openNativeNotifications, function(i, nativeNotification){
					nativeNotification.close();
				});
			});
		}

		function enable() {
			if (global.Notification && global.Notification.permission !== "granted") {
				global.Notification.requestPermission(function (status) {
					if (global.Notification.permission !== status) {
						global.Notification.permission = status;
					}
				});
			}
		}

		function notify(options) {
			settings = $.extend({}, {
				key: null,
				title: null,
				body: null,
				iconUrl: null,
				tag: null,
				onclick: null,
				onclose: null,
				onshow: null,
				hideAfter: 2000
			}, options);

			var renderNotification = function () {
				var note;
				if (global.Notification && global.Notification.permission === "granted") {
					note = new global.Notification(settings.title, {
						icon: settings.iconUrl || "",
						body: settings.body || "",
						tag: settings.tag
					});
					if (settings.onclick) {
						note.onclick = function () {
							global.focus();
							settings.onclick();
						};
					}
					if (settings.onclose) { note.onclose = settings.onclose; }
					if (settings.onshow) { note.onshow = settings.onshow; }
				}
				if (note) {
					openNativeNotifications.push(note);
					setTimeout(function () {
						if (note.close) {
							note.close();
							openNativeNotifications.splice(openNativeNotifications.indexOf(note), 1);
						}
					}, settings.hideAfter);
					registerUnloadCleanup();
				}
			};

			// if there's a unique key, only raise once per all tabs
			if (settings.key) {
				doOnce(settings.key, renderNotification);
			} else {
				renderNotification();
			}
		};

		return function () {
			// attempt to request permission on user gesture if not already granted
			$(function () {
				$('body').one('click', enable)
					.one('keydown', enable);
			});
			return {
				notify: notify
			};
		}

	})();

	var api = {
		register: function (options) {

			var nativeNotifier;
			if (options.native && !nativeNotifier) {
				nativeNotifier = NativeNotifier();
			}

			$.telligent.evolution.messaging.subscribe('notification.raised', function (data) {
				if(data.suppress === true)
					return;

				$.telligent.evolution.notifications.show(data.message, {
					id: data.id,
					duration: options.duration,
					mode: options.mode,
					onClose: function () {
						return $.telligent.evolution.put({
							url: $.telligent.evolution.site.getBaseUrl() + 'api.ashx/v2/notification/{NotificationId}.json',
							data: {
								NotificationId: data.id,
								MarkAsRead: true
							}
						});
					},
					onClick: function () {
						return $.telligent.evolution.put({
							url: $.telligent.evolution.site.getBaseUrl() + 'api.ashx/v2/notification/{NotificationId}.json',
							data: {
								NotificationId: data.id,
								MarkAsRead: true
							}
						}).then(function () {
							try {
								$.telligent.evolution.url.navigateTo(data.contentUrl);
							} catch (e) {
								window.location.href = data.contentUrl;
							}
						});
					}
				});

				if (options.native) {
					nativeNotifier.notify({
						key: (data.id + data.contentUrl + data.message),
						title: $.telligent.evolution.html.decode(data.message),
						iconUrl: data.avatarUrl,
						tag: 'notification-' + data.id,
						hideAfter: options.duration,
						onclick: function () {
							try {
								$.telligent.evolution.url.navigateTo(data.contentUrl);
							} catch (e) {
								window.location.href = data.contentUrl;
							}
						}
					});
				}
			});
		}
	};

	$.telligent = $.telligent || {};
	$.telligent.evolution = $.telligent.evolution || {};
	$.telligent.evolution.widgets = $.telligent.evolution.widgets || {};
	$.telligent.evolution.widgets.userNotifications = api;

})(jQuery, window);

