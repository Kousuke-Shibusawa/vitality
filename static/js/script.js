const onChangeInputFile = (e) => {
    if (e.target.files && e.target.files[0]) {
      const reader = new FileReader();
      reader.onload = function(e) {
        document.getElementById('thumbnail').setAttribute('src', e.target.result);
      };
      reader.readAsDataURL(e.target.files[0]);
    }
  };

<script type="text/javascript">
function submitbtn() {
    // 「OK」ボタン押下時
    if (confirm('実行しますか？')) {
        alert('OK');
    }
    // 「キャンセル」ボタン押下時
    else {
        alert('キャンセル');
    }
}
</script>