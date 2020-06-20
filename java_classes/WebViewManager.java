package org.bitdust_io.bitdust1;


import java.io.BufferedReader;
import java.io.BufferedInputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.File;
import java.io.OutputStream;
import java.io.IOException;
import java.io.UnsupportedEncodingException;

import java.lang.reflect.InvocationTargetException;
import java.lang.UnsatisfiedLinkError;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Iterator;
import java.util.List;
import java.util.Timer;
import java.util.TimerTask;
import java.net.URL;
import java.net.URLEncoder;
import java.net.HttpURLConnection;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.content.pm.PackageManager;
import android.content.pm.ApplicationInfo;
import android.provider.MediaStore;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Color;
import android.graphics.PixelFormat;
import android.Manifest;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Build;
import android.os.PowerManager;
import android.os.Process;
import android.util.Log;
import android.view.SurfaceHolder;
import android.view.SurfaceView;
import android.view.View;
import android.view.ViewGroup;
import android.view.ViewGroup.LayoutParams;
import android.view.Window;
import android.view.WindowManager;
import android.widget.ImageView;
import android.widget.Toast;

import android.webkit.ConsoleMessage;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

import org.libsdl.app.SDL;
import org.libsdl.app.SDLActivity;

import org.kivy.android.PythonActivity;
import org.kivy.android.PythonUtil;
import org.kivy.android.launcher.Project;

import org.renpy.android.ResourceManager;
import org.renpy.android.AssetExtract;


public class WebViewManager {

    private static final String TAG = "WebViewManager";

    private static boolean appliedWindowedModeHack = false;
    private static final int INPUT_FILE_REQUEST_CODE = 10001;
    public WebView webView = null;
    private WebSettings webSettings = null;
    private ValueCallback<Uri[]> mUploadMessage = null;

    public void createWebView(Activity activity) {
        Log.v(TAG, "createWebView()");
        try {
            this.webView = new WebView(activity);
            Log.v(TAG, "createWebView() 1");
            webSettings = this.webView.getSettings();
            Log.v(TAG, "createWebView() 2");
            webSettings.setJavaScriptEnabled(true);
            webSettings.setUseWideViewPort(true);
            webSettings.setLoadWithOverviewMode(true);
            webSettings.setAllowFileAccess(true);
            webSettings.setAllowContentAccess(true);
            webSettings.setAllowFileAccessFromFileURLs(true);
            webSettings.setAllowUniversalAccessFromFileURLs(true);
            webSettings.setSupportZoom(false);
            webSettings.setBuiltInZoomControls(false);
            webSettings.setAppCacheEnabled(false);
            this.webView.setWebContentsDebuggingEnabled(true);
            Log.v(TAG, "createWebView() 3");
            this.webView.setWebViewClient(new MyWebViewClient());
            Log.v(TAG, "createWebView() 4");
            this.webView.setWebChromeClient(new MyWebChromeClient());
            Log.v(TAG, "createWebView() 5");
            // this.webView.requestFocus(View.FOCUS_DOWN);
            //if SDK version is greater of 19 then activate hardware acceleration otherwise activate software acceleration
            if (Build.VERSION.SDK_INT >= 19) {
                this.webView.setLayerType(View.LAYER_TYPE_HARDWARE, null);
            } else if (Build.VERSION.SDK_INT >= 11 && Build.VERSION.SDK_INT < 19) {
                this.webView.setLayerType(View.LAYER_TYPE_SOFTWARE, null);
            }
            Log.v(TAG, "createWebView() 6");
            activity.addContentView(this.webView, new LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT));
            Log.v(TAG, "createWebView() ok");
        } catch (Exception exc) {
            Log.e(TAG, "Failed creating WebView: " + exc);
        }
    }


//    public String getImagePath(Uri uri) {
//        Log.v(TAG, "getImagePath()");
//        Cursor cursor = getContentResolver().query(uri, null, null, null, null);
//        cursor.moveToFirst();
//        String document_id = cursor.getString(0);
//        document_id = document_id.substring(document_id.lastIndexOf(":")+1);
//        cursor.close();
//        cursor = getContentResolver().query(
//            android.provider.MediaStore.Images.Media.EXTERNAL_CONTENT_URI,
//            null,
//            MediaStore.Images.Media._ID + " = ? ",
//            new String[]{document_id},
//            null
//        );
//        cursor.moveToFirst();
//        String path = cursor.getString(cursor.getColumnIndex(MediaStore.Images.Media.DATA));
//        cursor.close();
//        return path;
//    }


//    protected void parseSelectedFilePath(int resultCode, Intent intent) {
//        Log.v(TAG, "parseSelectedFilePath()");
//        Uri[] results = null;
//        if (resultCode == RESULT_OK && intent != null) {
//            Log.v(TAG, "PythonActivity is running parseSelectedFilePath for " + intent.getData());
//            results  = new Uri[1];
//            try {
//                String full_path = getImagePath(intent.getData());
//                String encoded_path = URLEncoder.encode(full_path, "UTF-8");
//                File fake_file = new File("file:///" + encoded_path);
//                results[0] = Uri.fromFile(fake_file);
//                Log.v(TAG, "PythonActivity parseSelectedFilePath : " + results[0].toString());
//            } catch (UnsupportedEncodingException exc) {
//                Log.e(TAG, "PythonActivity parseSelectedFilePath error encoding file path");
//            }
//        }
//        else {
//            Log.v(TAG, "PythonActivity is running parseSelectedFilePath return EMPTY LIST: resultCode=" + resultCode + " intent=" + intent);
//        }
//        mUploadMessage.onReceiveValue(results);
//        mUploadMessage = null;
//    }


    public class MyWebChromeClient extends WebChromeClient {

//        public boolean onShowFileChooser(WebView view, ValueCallback<Uri[]> filePath, WebChromeClient.FileChooserParams fileChooserParams) {
//            Log.v(TAG, "onShowFileChooser()");
//            if (mUploadMessage != null) {
//                Log.v(TAG, "PythonActivity mUploadMessage is not empty");
//                mUploadMessage.onReceiveValue(null);
//            }
//            mUploadMessage = filePath;
//            Intent contentSelectionIntent = new Intent(Intent.ACTION_GET_CONTENT);
//            contentSelectionIntent.addCategory(Intent.CATEGORY_OPENABLE);
//            contentSelectionIntent.setType("*/*");
//            contentSelectionIntent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, false);
//            Intent[] intentArray;
//            intentArray = new Intent[0];
//            Intent chooserIntent = new Intent(Intent.ACTION_CHOOSER);
//            chooserIntent.putExtra(Intent.EXTRA_INTENT, contentSelectionIntent);
//            chooserIntent.putExtra(Intent.EXTRA_TITLE, "Select file to upload");
//            chooserIntent.putExtra(Intent.EXTRA_INITIAL_INTENTS, intentArray);
//            //startActivityForResult(Intent.createChooser(chooserIntent, "Select file"), INPUT_FILE_REQUEST_CODE);
//            startActivityForResult(chooserIntent, INPUT_FILE_REQUEST_CODE);
//            return true;
//        }

        @Override
        public boolean onConsoleMessage(ConsoleMessage consoleMessage) {
            Log.v("WebViewConsole", consoleMessage.message());
            return true;
        }
    }

    public class MyWebViewClient extends WebViewClient {

    }


    public void recursiveDelete(File f) {
        if (f.isDirectory()) {
            for (File r : f.listFiles()) {
                recursiveDelete(r);
            }
        }
        f.delete();
    }


    private class HttpRequestGET extends AsyncTask<String, Void, String> {
        @Override
        protected void onPreExecute() {
            super.onPreExecute();
            Log.v(TAG, "HttpRequestGET.onPreExecute()");
        }

        @Override
        protected String doInBackground(String... urls) {
            Log.v(TAG, "HttpRequestGET.doInBackground() " + urls[0]);
            String result = "";
            try {
                URL url = new URL(urls[0]);
                HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
                urlConnection.setRequestMethod("GET");
                urlConnection.setUseCaches(false);
                urlConnection.setAllowUserInteraction(false);
                urlConnection.setConnectTimeout(300);
                urlConnection.setReadTimeout(300);
                urlConnection.setRequestProperty("Content-Type", "application/json; utf-8");
                urlConnection.setRequestProperty("Content-length", "0");
                urlConnection.setRequestProperty("Accept", "application/json");
                urlConnection.connect();
                try {
                    int responseCode = urlConnection.getResponseCode();
                    if (responseCode == HttpURLConnection.HTTP_OK) {
                        BufferedReader br = new BufferedReader(new InputStreamReader(urlConnection.getInputStream(), "utf-8"));
                        StringBuilder sb = new StringBuilder();
                        String line;
                        while ((line = br.readLine()) != null) {
                            sb.append(line + "\n");
                        }
                        br.close();
                        result = sb.toString();
                    }
                } catch (Exception exc) {
                    Log.e(TAG, "HttpRequestGET.doInBackground() FAILED reading: " + exc);
                }
                urlConnection.disconnect();
            }
            catch (Exception exc) {
                Log.e(TAG, "HttpRequestGET.doInBackground() FAILED connecting: " + exc);
            }
            return result;
        }

        @Override
        protected void onPostExecute(String result) {
            Log.v(TAG, "HttpRequestGET.onPostExecute() OK");
        }
    }

    public String requestGetURL(String url_str) {
        Log.v(TAG, "requestGetURL() " + url_str);
        String str_result = "";
        try {
            str_result = new HttpRequestGET().execute(url_str).get();
        } catch (Exception exc) {
            Log.e(TAG, "requestGetURL() FAILED : " + exc);
        }
        Log.v(TAG, "requestGetURL() result : " + str_result);
        return str_result;
    }

}
