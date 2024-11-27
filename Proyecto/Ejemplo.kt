CONSTRUCTOR DEL INTENT: // Intent explícito
Intent intent = new Intent(context, TargetActivity.class);

// Intent implícito
Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse("http://example.com"));