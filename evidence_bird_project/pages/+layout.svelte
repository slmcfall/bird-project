<script>
	import '@evidence-dev/tailwind/fonts.css';
	import '../app.css';
	import { EvidenceDefaultLayout } from '@evidence-dev/core-components';
	export let data;
</script>

<EvidenceDefaultLayout {data} logo="/birdweather-logo.svg" homePageName="birds birds birds!">
	<slot slot="content" />
</EvidenceDefaultLayout>
