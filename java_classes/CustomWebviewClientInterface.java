package com.razzbee.WebviewEngine;

import android.webkit.WebView;
import android.webkit.ConsoleMessage;
import java.lang.String;
import android.graphics.Bitmap;


public interface CustomWebviewClientInterface{

	public boolean shouldOverrideUrlLoading(WebView view, String url);

    public void onPageStarted(WebView view, String url, Bitmap favicon);

    public void onPageFinished(WebView view, String url);

    public void onPageCommitVisible(WebView view, String url);

    public void onReceivedError(WebView view, int errorCode, String description, String failingUrl);

    public boolean onConsoleMessage(ConsoleMessage consoleMessage);

}
